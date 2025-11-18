#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.enforcement.schema_validator (v1.1 Canonical Edition)

Runtime schema validation for PLD events and envelopes.

- Prefers repository schemas in pld_runtime/01_schemas/
- Falls back to minimal internal schemas if files are missing or invalid
- Designed for use by detectors, controllers, and CLI tools

This module does NOT perform any sequencing / temporal checks.
It only enforces structural consistency.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    import jsonschema
    from jsonschema import Draft7Validator
    HAS_JSONSCHEMA = True
except Exception:  # pragma: no cover - optional dependency
    HAS_JSONSCHEMA = False


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
# Canonical schema location within pld_runtime
SCHEMAS_DIR = HERE.parent / "01_schemas"

DEFAULT_EVENT_SCHEMA_PATH = SCHEMAS_DIR / "pld_event.schema.json"
DEFAULT_ENVELOPE_SCHEMA_PATH = SCHEMAS_DIR / "runtime_event_envelope.json"


# ---------------------------------------------------------------------------
# Fallback Schemas (minimal but sound)
# ---------------------------------------------------------------------------

_FALLBACK_PLDEVENT_SCHEMA: Dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "PLD Runtime Event (fallback)",
    "type": "object",
    "required": ["event_id", "timestamp", "session_id", "event_type"],
    "properties": {
        "event_id": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "session_id": {"type": "string"},
        "turn_id": {"type": "string"},
        "source": {"type": "string"},
        "event_type": {"type": "string"},
        "pld": {"type": "object"},
        "payload": {"type": "object"},
        "runtime": {"type": "object"}
    },
    "additionalProperties": True
}

_FALLBACK_ENVELOPE_SCHEMA: Dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "PLD Runtime Event Envelope (fallback)",
    "type": "object",
    "required": ["envelope_id", "timestamp", "session", "trace", "runtime", "event"],
    "properties": {
        "envelope_id": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "session": {"type": "object"},
        "trace": {"type": "object"},
        "runtime": {"type": "object"},
        "event": {"type": "object"}
    },
    "additionalProperties": True
}


# ---------------------------------------------------------------------------
# Result Types
# ---------------------------------------------------------------------------

@dataclass
class SchemaError:
    """Single schema violation."""
    path: str
    message: str
    validator: Optional[str] = None
    validator_value: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "message": self.message,
            "validator": self.validator,
            "validator_value": self.validator_value,
        }


@dataclass
class ValidationResult:
    """Schema validation result."""
    ok: bool
    schema_name: str
    errors: List[SchemaError]
    used_fallback: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "schema_name": self.schema_name,
            "used_fallback": self.used_fallback,
            "errors": [e.to_dict() for e in self.errors],
        }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_validator(
    primary_path: Path,
    fallback_schema: Dict[str, Any],
    label: str,
) -> tuple[Optional["Draft7Validator"], bool]:
    """
    Try to build a Draft7Validator from a primary schema file.
    Fall back to the provided in-memory schema if unavailable or invalid.

    Returns (validator_or_none, used_fallback).
    """
    if not HAS_JSONSCHEMA:
        # Validation will be logically "ok" but structurally unchecked.
        return None, True

    schema: Dict[str, Any]
    used_fallback = False

    if primary_path.exists():
        try:
            schema = _load_json(primary_path)
        except Exception as e:  # pragma: no cover - I/O error path
            print(
                f"[warn] Failed to read {label} schema at {primary_path}: {e}\n"
                "       Falling back to embedded minimal schema.",
                file=sys.stderr,
            )
            schema = fallback_schema
            used_fallback = True
    else:
        print(
            f"[info] {label} schema not found at {primary_path}. "
            "Using embedded minimal schema.",
            file=sys.stderr,
        )
        schema = fallback_schema
        used_fallback = True

    try:
        validator = Draft7Validator(schema)
    except Exception as e:  # pragma: no cover - invalid schema path
        print(
            f"[warn] {label} schema is invalid: {e}\n"
            "       Falling back to embedded minimal schema.",
            file=sys.stderr,
        )
        validator = Draft7Validator(fallback_schema)
        used_fallback = True

    return validator, used_fallback


# ---------------------------------------------------------------------------
# Validators (lazy singletons)
# ---------------------------------------------------------------------------

_EVENT_VALIDATOR: Optional["Draft7Validator"] = None
_EVENT_VALIDATOR_FALLBACK: bool = False

_ENVELOPE_VALIDATOR: Optional["Draft7Validator"] = None
_ENVELOPE_VALIDATOR_FALLBACK: bool = False


def _ensure_event_validator() -> None:
    global _EVENT_VALIDATOR, _EVENT_VALIDATOR_FALLBACK

    if _EVENT_VALIDATOR is not None:
        return

    validator, used_fallback = _build_validator(
        primary_path=DEFAULT_EVENT_SCHEMA_PATH,
        fallback_schema=_FALLBACK_PLDEVENT_SCHEMA,
        label="PLD event",
    )
    _EVENT_VALIDATOR = validator
    _EVENT_VALIDATOR_FALLBACK = used_fallback


def _ensure_envelope_validator() -> None:
    global _ENVELOPE_VALIDATOR, _ENVELOPE_VALIDATOR_FALLBACK

    if _ENVELOPE_VALIDATOR is not None:
        return

    validator, used_fallback = _build_validator(
        primary_path=DEFAULT_ENVELOPE_SCHEMA_PATH,
        fallback_schema=_FALLBACK_ENVELOPE_SCHEMA,
        label="PLD envelope",
    )
    _ENVELOPE_VALIDATOR = validator
    _ENVELOPE_VALIDATOR_FALLBACK = used_fallback


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_event(
    obj: Dict[str, Any],
    *,
    schema_path: Optional[Union[str, Path]] = None,
) -> ValidationResult:
    """
    Validate a single PLD event object against the event schema.

    If schema_path is given, it overrides the default location.
    Falls back to a minimal schema when appropriate.
    """
    if not HAS_JSONSCHEMA:
        # Structural validation disabled, but we still indicate success.
        return ValidationResult(
            ok=True,
            schema_name="pld_event (no-jsonschema)",
            errors=[],
            used_fallback=True,
        )

    if schema_path is not None:
        validator, used_fallback = _build_validator(
            primary_path=Path(schema_path),
            fallback_schema=_FALLBACK_PLDEVENT_SCHEMA,
            label="PLD event (override)",
        )
    else:
        _ensure_event_validator()
        validator = _EVENT_VALIDATOR
        used_fallback = _EVENT_VALIDATOR_FALLBACK

    assert validator is not None  # for type checkers

    errors: List[SchemaError] = []
    for e in validator.iter_errors(obj):
        path_str = ".".join(str(p) for p in e.path) or "<root>"
        errors.append(
            SchemaError(
                path=path_str,
                message=e.message,
                validator=e.validator,
                validator_value=e.validator_value,
            )
        )

    return ValidationResult(
        ok=not errors,
        schema_name="pld_event",
        errors=errors,
        used_fallback=used_fallback,
    )


def validate_envelope(
    obj: Dict[str, Any],
    *,
    schema_path: Optional[Union[str, Path]] = None,
) -> ValidationResult:
    """
    Validate a single PLD runtime envelope object.

    If schema_path is given, it overrides the default location.
    """
    if not HAS_JSONSCHEMA:
        return ValidationResult(
            ok=True,
            schema_name="runtime_event_envelope (no-jsonschema)",
            errors=[],
            used_fallback=True,
        )

    if schema_path is not None:
        validator, used_fallback = _build_validator(
            primary_path=Path(schema_path),
            fallback_schema=_FALLBACK_ENVELOPE_SCHEMA,
            label="PLD envelope (override)",
        )
    else:
        _ensure_envelope_validator()
        validator = _ENVELOPE_VALIDATOR
        used_fallback = _ENVELOPE_VALIDATOR_FALLBACK

    assert validator is not None  # for type checkers

    errors: List[SchemaError] = []
    for e in validator.iter_errors(obj):
        path_str = ".".join(str(p) for p in e.path) or "<root>"
        errors.append(
            SchemaError(
                path=path_str,
                message=e.message,
                validator=e.validator,
                validator_value=e.validator_value,
            )
        )

    return ValidationResult(
        ok=not errors,
        schema_name="runtime_event_envelope",
        errors=errors,
        used_fallback=used_fallback,
    )


def validate_jsonl_file(
    path: Union[str, Path],
    *,
    envelope_mode: bool = False,
    schema_path: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    """
    Validate a JSONL file containing either bare PLD events
    or full runtime envelopes.

    Returns a summary dict:

    {
      "ok": bool,
      "total": int,
      "valid": int,
      "invalid": int,
      "errors": [ {line, path, message, ...}, ... ],
      "used_fallback": bool
    }
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))

    total = 0
    valid = 0
    invalid = 0
    used_fallback_any = False
    error_list: List[Dict[str, Any]] = []

    with p.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            total += 1
            try:
                obj = json.loads(line)
            except Exception as e:
                invalid += 1
                error_list.append(
                    {
                        "line": idx,
                        "path": "<parse>",
                        "message": f"Invalid JSON: {e}",
                    }
                )
                continue

            if envelope_mode:
                result = validate_envelope(obj, schema_path=schema_path)
            else:
                result = validate_event(obj, schema_path=schema_path)

            used_fallback_any = used_fallback_any or result.used_fallback

            if result.ok:
                valid += 1
            else:
                invalid += 1
                for err in result.errors:
                    error_list.append(
                        {
                            "line": idx,
                            **err.to_dict(),
                        }
                    )

    return {
        "ok": invalid == 0,
        "total": total,
        "valid": valid,
        "invalid": invalid,
        "errors": error_list,
        "used_fallback": used_fallback_any,
    }


__all__ = [
    "SchemaError",
    "ValidationResult",
    "validate_event",
    "validate_envelope",
    "validate_jsonl_file",
]
