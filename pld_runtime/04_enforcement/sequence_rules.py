"""
# version: 2.0
# status: runtime
# authority: Level 5 — runtime implementation (reads Level 1–3 specifications)
# purpose: Enforces sequence and ordering rules for PLD events and sessions.
# scope: Provides session grouping, temporal semantics, and drift/repair/reentry checks for validator-layer use only.
# dependencies: Read-only PLD lifecycle, schema, event matrix, and metrics specifications (Levels 1–3).
# change_classification: runtime-only, non-breaking (patch-level import fix for sandbox execution)

"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

# ValidationMode SHOULD come from the canonical schema_validator module.
# In sandbox / script-only environments there may be no package context, so
# we avoid relative imports here and instead try an absolute import first,
# then fall back to a local definition for standalone execution.
try:  # pragma: no cover - primary absolute import
    from schema_validator import ValidationMode  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover - sandbox / standalone fallback
    # NOTE: Migration difference
    # This local definition exists solely so this module can be executed
    # in isolation (e.g., notebooks, sandboxes). In production, the
    # canonical ValidationMode from schema_validator MUST be used.
    class ValidationMode(str, Enum):  # type: ignore[no-redef]
        STRICT = "strict"
        WARN = "warn"
        NORMALIZE = "normalize"


Json = Mapping[str, Any]
MutableJson = MutableMapping[str, Any]

# ---------------------------------------------------------------------------
# Issue Model (New canonical structure)
# ---------------------------------------------------------------------------


class SequenceIssueSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class SequenceIssue:
    """
    A single temporal / ordering anomaly.

    NOTE: normalized naming replaces v1.1 "SequenceViolation",
    but remains semantically equivalent.
    """

    code: str
    message: str
    session_id: Optional[str]
    index: Optional[int]
    turn_sequence: Optional[int]
    severity: SequenceIssueSeverity
    rule: Optional[str] = None

    def is_error(self) -> bool:
        return self.severity == SequenceIssueSeverity.ERROR


@dataclass
class SessionSequenceView:
    """Per-session ordered representation of validated events."""

    session_id: str
    events: List[MutableJson]
    issues: List[SequenceIssue]


@dataclass
class SequenceCheckResult:
    """Aggregate temporal validation result across sessions."""

    mode: ValidationMode
    sessions: List[SessionSequenceView]
    issues: List[SequenceIssue]

    @property
    def valid(self) -> bool:
        return not any(i.is_error() for i in self.issues)


# ---------------------------------------------------------------------------
# Optional configuration (Merged from legacy)
# ---------------------------------------------------------------------------

@dataclass
class TemporalRuleConfig:
    """
    Optional timing-based lifecycle checks derived from legacy v1.1.

    These rules are NOT normative and MUST be opt-in.
    They MAY be disabled without affecting structural validity.

    All thresholds are in milliseconds.
    """

    max_drift_to_repair_ms: int = 30000
    max_repair_to_reentry_ms: int = 30000
    require_repair_for_drift: bool = True
    require_reentry_after_repair: bool = True
    allow_reentry_without_repair: bool = False


# ---------------------------------------------------------------------------
# Internal event helpers
# ---------------------------------------------------------------------------


def _get_session_id(event: Json) -> Optional[str]:
    value = event.get("session_id")
    return str(value) if value is not None else None


def _get_turn_sequence(event: Json) -> Optional[int]:
    value = event.get("turn_sequence")
    if isinstance(value, int):
        return value
    return None


def _sort_events_by_turn_sequence(events: Sequence[Json]) -> List[MutableJson]:
    """Primary authoritative ordering rule.

    `turn_sequence` MUST define timeline sorting for valid events.

    Events with missing or non-integer `turn_sequence` are appended at the end
    in original order. This is a **best-effort** ordering helper for potentially
    invalid data; strict validation is still performed separately and will flag
    such events as errors.
    """

    indexed: List[Tuple[int, int, Json]] = []
    tail: List[Json] = []

    for idx, ev in enumerate(events):
        ts = _get_turn_sequence(ev)
        if ts is None:
            tail.append(ev)
        else:
            indexed.append((ts, idx, ev))

    indexed.sort(key=lambda t: (t[0], t[1]))
    ordered: List[MutableJson] = [dict(ev) for (_, _, ev) in indexed]
    ordered.extend(dict(ev) for ev in tail)
    return ordered


# ---------------------------------------------------------------------------
# Legacy-compatible timestamp utilities (retained where compatible)
# ---------------------------------------------------------------------------


def _parse_ts(ts: Any) -> Optional[datetime]:
    """Parse RFC3339 / ISO8601 timestamps, including 'Z'.

    # TODO: Review required (uncertain alignment)
    # Timezone Naivety:
    # - datetime.fromisoformat handles offsets, but naive strings are interpreted
    #   in the local system timezone when calling astimezone(timezone.utc).
    # - Clarify whether PLD events MUST provide timezone-aware timestamps
    #   (Z or ±offset) or whether naive timestamps should be treated as UTC.
    """
    if not isinstance(ts, str):
        return None
    try:
        s = ts
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            # NOTE: For now we rely on system-local interpretation; see TODO above.
            return dt.astimezone(timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def _ms_between(a: datetime, b: datetime) -> float:
    return (b - a).total_seconds() * 1000.0


# ---------------------------------------------------------------------------
# Core enforcement rules
# ---------------------------------------------------------------------------


def _check_monotonic_turn_sequence(session_id: str, events: List[MutableJson]) -> List[SequenceIssue]:
    """MUST rule: turn_sequence MUST be strictly increasing within session."""

    issues: List[SequenceIssue] = []
    last_ts: Optional[int] = None

    for idx, ev in enumerate(events):
        ts = _get_turn_sequence(ev)

        if ts is None:
            issues.append(
                SequenceIssue(
                    code="TURN_SEQUENCE_MISSING",
                    message="Event missing turn_sequence; ordering ambiguous.",
                    session_id=session_id,
                    index=idx,
                    turn_sequence=None,
                    severity=SequenceIssueSeverity.ERROR,
                    rule="pld_event.turn_sequence.required",
                )
            )
            continue

        if ts < 1:
            issues.append(
                SequenceIssue(
                    code="TURN_SEQUENCE_OUT_OF_RANGE",
                    message=f"turn_sequence MUST be ≥1 (found {ts}).",
                    session_id=session_id,
                    index=idx,
                    turn_sequence=ts,
                    severity=SequenceIssueSeverity.ERROR,
                    rule="pld_event.turn_sequence.domain",
                )
            )

        if last_ts is not None:
            if ts == last_ts:
                issues.append(
                    SequenceIssue(
                        code="TURN_SEQUENCE_DUPLICATE",
                        message=f"Duplicate turn_sequence {ts} detected.",
                        session_id=session_id,
                        index=idx,
                        turn_sequence=ts,
                        severity=SequenceIssueSeverity.ERROR,
                        rule="metrics.event_ordering.unique",
                    )
                )
            elif ts < last_ts:
                issues.append(
                    SequenceIssue(
                        code="TURN_SEQUENCE_NON_MONOTONIC",
                        message=f"Non-monotonic ordering detected ({ts} < {last_ts}).",
                        session_id=session_id,
                        index=idx,
                        turn_sequence=ts,
                        severity=SequenceIssueSeverity.ERROR,
                        rule="metrics.event_ordering.monotonic",
                    )
                )

        last_ts = ts

    return issues


# ---------------------------------------------------------------------------
# Optional lifecycle timing checks (merged from legacy v1.1)
# ---------------------------------------------------------------------------


def _apply_temporal_lifecycle_rules(
    session_id: str,
    events: List[MutableJson],
    config: TemporalRuleConfig,
) -> List[SequenceIssue]:
    """Implements drift→repair→reentry timing rules from v1.1.

    # NOTE: Migration difference
    # - Only executed if explicitly enabled by caller.
    """

    issues: List[SequenceIssue] = []

    active_drift_ts: Optional[datetime] = None
    active_repair_ts: Optional[datetime] = None

    for idx, ev in enumerate(events):
        pld = ev.get("pld") or {}
        phase = str(pld.get("phase", "")).lower()
        ts = _parse_ts(ev.get("timestamp"))

        if ts is None:
            continue

        # Drift detected
        if phase == "drift":
            if active_drift_ts is not None and config.require_repair_for_drift:
                issues.append(
                    SequenceIssue(
                        code="DRIFT_CHAIN",
                        message="Drift occurred before previous drift was repaired.",
                        session_id=session_id,
                        index=idx,
                        turn_sequence=_get_turn_sequence(ev),
                        severity=SequenceIssueSeverity.WARNING,
                        rule="runtime.temporal.drift_chain",
                    )
                )
            active_drift_ts = ts
            active_repair_ts = None

        # Repair detected
        elif phase == "repair":
            if active_drift_ts is None:
                if config.require_repair_for_drift:
                    issues.append(
                        SequenceIssue(
                            code="REPAIR_WITHOUT_DRIFT",
                            message="Repair without preceding drift.",
                            session_id=session_id,
                            index=idx,
                            turn_sequence=_get_turn_sequence(ev),
                            severity=SequenceIssueSeverity.ERROR,
                            rule="runtime.temporal.repair_without_drift",
                        )
                    )
            else:
                dt = _ms_between(active_drift_ts, ts)
                if dt > config.max_drift_to_repair_ms:
                    issues.append(
                        SequenceIssue(
                            code="DRIFT_TIMEOUT",
                            message=f"Repair occurred after {dt:.1f}ms delay.",
                            session_id=session_id,
                            index=idx,
                            turn_sequence=_get_turn_sequence(ev),
                            severity=SequenceIssueSeverity.WARNING,
                            rule="runtime.temporal.drift_timeout",
                        )
                    )
                active_repair_ts = ts

        # Reentry detected
        elif phase == "reentry":
            if active_repair_ts is None and not config.allow_reentry_without_repair:
                issues.append(
                    SequenceIssue(
                        code="REENTRY_WITHOUT_REPAIR",
                        message="Reentry without preceding repair.",
                        session_id=session_id,
                        index=idx,
                        turn_sequence=_get_turn_sequence(ev),
                        severity=SequenceIssueSeverity.ERROR,
                        rule="runtime.temporal.reentry_without_repair",
                    )
                )
            elif active_repair_ts is not None:
                dt = _ms_between(active_repair_ts, ts)
                if dt > config.max_repair_to_reentry_ms:
                    issues.append(
                        SequenceIssue(
                            code="REPAIR_TIMEOUT",
                            message=f"Reentry occurred after {dt:.1f}ms delay.",
                            session_id=session_id,
                            index=idx,
                            turn_sequence=_get_turn_sequence(ev),
                            severity=SequenceIssueSeverity.WARNING,
                            rule="runtime.temporal.repair_timeout",
                        )
                    )

            active_drift_ts = None
            active_repair_ts = None

    return issues


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def group_events_by_session(events: Iterable[Json]) -> Dict[str, List[MutableJson]]:
    """Group events by `session_id` and sort each group by `turn_sequence`.

    # TODO: Review required (uncertain alignment)
    # Session Grouping Memory Usage:
    # - Current implementation buffers all events in memory per session.
    # - For large production logs, a streaming / windowed approach may be
    #   required (e.g., using itertools.groupby over pre-sorted input).
    """
    buffer: Dict[str, List[Json]] = {}
    for ev in events:
        sid = _get_session_id(ev) or "<unknown>"
        buffer.setdefault(sid, []).append(ev)

    grouped: Dict[str, List[MutableJson]] = {}
    for sid, evs in buffer.items():
        grouped[sid] = _sort_events_by_turn_sequence(evs)

    return grouped


def check_sequence_rules(
    events: Iterable[Json],
    *,
    mode: ValidationMode = ValidationMode.STRICT,
    temporal_rules: Optional[TemporalRuleConfig] = None,
) -> SequenceCheckResult:
    """Core validation entrypoint.

    - Always enforces ordering rules.
    - Optionally enforces lifecycle timing semantics.
    """

    grouped = group_events_by_session(events)
    sessions: List[SessionSequenceView] = []
    all_issues: List[SequenceIssue] = []

    for sid, evs in grouped.items():
        issues: List[SequenceIssue] = []

        # MUST ordering enforcement
        issues.extend(_check_monotonic_turn_sequence(sid, evs))

        # Optional lifecycle timing rules (legacy compatibility path)
        if temporal_rules is not None:
            issues.extend(_apply_temporal_lifecycle_rules(sid, evs, temporal_rules))

        sessions.append(SessionSequenceView(session_id=sid, events=evs, issues=issues))
        all_issues.extend(issues)

    return SequenceCheckResult(mode=mode, sessions=sessions, issues=all_issues)


# ---------------------------------------------------------------------------
# Simple self-checks / examples (ad hoc tests)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Basic happy-path: strictly increasing turn_sequence, no lifecycle phases.
    events_ok = [
        {"session_id": "s1", "turn_sequence": 1, "timestamp": "2024-01-01T00:00:00Z"},
        {"session_id": "s1", "turn_sequence": 2, "timestamp": "2024-01-01T00:00:01Z"},
    ]
    result_ok = check_sequence_rules(events_ok)
    print("[TEST] monotonic sequence valid?", result_ok.valid)

    # Non-monotonic turn_sequence should produce errors.
    events_bad = [
        {"session_id": "s2", "turn_sequence": 2, "timestamp": "2024-01-01T00:00:01Z"},
        {"session_id": "s2", "turn_sequence": 1, "timestamp": "2024-01-01T00:00:02Z"},
    ]
    result_bad = check_sequence_rules(events_bad)
    print("[TEST] non-monotonic sequence valid?", result_bad.valid)
    for issue in result_bad.issues:
        print(" -", issue.code, issue.message)

    # Drift→repair→reentry timing path (temporal rules enabled).
    events_temporal = [
        {
            "session_id": "s3",
            "turn_sequence": 1,
            "timestamp": "2024-01-01T00:00:00Z",
            "pld": {"phase": "drift"},
        },
        {
            "session_id": "s3",
            "turn_sequence": 2,
            "timestamp": "2024-01-01T00:00:05Z",
            "pld": {"phase": "repair"},
        },
        {
            "session_id": "s3",
            "turn_sequence": 3,
            "timestamp": "2024-01-01T00:00:10Z",
            "pld": {"phase": "reentry"},
        },
    ]
    temporal_cfg = TemporalRuleConfig()
    result_temporal = check_sequence_rules(events_temporal, temporal_rules=temporal_cfg)
    print("[TEST] temporal sequence valid?", result_temporal.valid)
    for issue in result_temporal.issues:
        print(" -", issue.code, issue.message)


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = [
    "ValidationMode",
    "SequenceIssueSeverity",
    "SequenceIssue",
    "SessionSequenceView",
    "SequenceCheckResult",
    "TemporalRuleConfig",
    "group_events_by_session",
    "check_sequence_rules",
]


# Deferred for later phase
# - Replace in-memory session grouping with a streaming or chunked mechanism
#   for large-scale production logs (e.g., itertools.groupby over sorted input).
# - Clarify and standardize handling of naive timestamps in _parse_ts, including
#   whether PLD events MUST be timezone-aware or whether naive times imply UTC.


