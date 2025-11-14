#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.failover.backoff_policies

Concept
-------
Central place for retry / backoff behavior definitions used during
failover and recovery.

This module provides:
    - Named backoff profiles (none / light / medium / heavy)
    - Pure functions to compute next delay and whether to continue
    - A small config model to plug into host runtimes

It does NOT:
    - perform retries itself
    - sleep or block
    - call external systems

Host runtimes should:
    - read FailoverDecision.metadata["backoff_profile"] (if present)
    - map it to a BackoffPolicy via this module
    - drive their own retry loop accordingly
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Tuple


# ---------------------------------------------------------------------------
# Backoff profile definitions
# ---------------------------------------------------------------------------

class BackoffProfile(str, Enum):
    """
    Named backoff profiles.

    - NONE:
        No backoff, no retries.

    - LIGHT:
        Few retries with small exponential delays.
        Suitable for transient errors.

    - MEDIUM:
        Moderate number of retries with exponential backoff.
        Use when downstream may be temporarily overloaded.

    - HEAVY:
        Conservative retries with larger delays and fewer attempts.
        Appropriate for severe or systemic issues.
    """

    NONE = "none"
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"


@dataclass
class BackoffPolicy:
    """
    Configuration for a backoff policy.

    Fields
    ------
    profile:
        Named profile.

    max_retries:
        Maximum number of attempts (excluding the initial one).
        Example: max_retries=3 → attempts 0,1,2,3 (4 total).

    base_delay_seconds:
        Base delay for an exponential schedule.

    multiplier:
        Exponential multiplier applied per attempt:
            delay = base_delay_seconds * (multiplier ** attempt)

        attempt is 1-based for the first retry:
            attempt=0 → 0 delay (no backoff before first call)
            attempt=1 → base_delay_seconds * multiplier
            attempt=2 → base_delay_seconds * multiplier^2
            ...

    jitter_ratio:
        Fraction of delay that host may use as +/- jitter range.
        This module does not generate random jitter; it only
        supplies the nominal delay.

    Notes
    -----
    The backoff schedule is deterministic and purely numerical;
    host systems are free to adjust it (e.g., adding randomness).
    """

    profile: BackoffProfile
    max_retries: int
    base_delay_seconds: float
    multiplier: float
    jitter_ratio: float = 0.1

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["profile"] = self.profile.value
        return d


# Canonical profile registry
_BACKOFF_POLICIES: Dict[BackoffProfile, BackoffPolicy] = {
    BackoffProfile.NONE: BackoffPolicy(
        profile=BackoffProfile.NONE,
        max_retries=0,
        base_delay_seconds=0.0,
        multiplier=1.0,
        jitter_ratio=0.0,
    ),
    BackoffProfile.LIGHT: BackoffPolicy(
        profile=BackoffProfile.LIGHT,
        max_retries=2,
        base_delay_seconds=0.5,
        multiplier=2.0,
        jitter_ratio=0.25,
    ),
    BackoffProfile.MEDIUM: BackoffPolicy(
        profile=BackoffProfile.MEDIUM,
        max_retries=3,
        base_delay_seconds=1.0,
        multiplier=2.0,
        jitter_ratio=0.25,
    ),
    BackoffProfile.HEAVY: BackoffPolicy(
        profile=BackoffProfile.HEAVY,
        max_retries=4,
        base_delay_seconds=2.0,
        multiplier=2.0,
        jitter_ratio=0.3,
    ),
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_backoff_policy(profile: str | BackoffProfile) -> BackoffPolicy:
    """
    Retrieve BackoffPolicy for a given profile name.

    Unknown profile names default to MEDIUM to remain conservative.
    """
    if isinstance(profile, str):
        try:
            profile_enum = BackoffProfile(profile.lower())
        except Exception:
            profile_enum = BackoffProfile.MEDIUM
    else:
        profile_enum = profile

    return _BACKOFF_POLICIES.get(profile_enum, _BACKOFF_POLICIES[BackoffProfile.MEDIUM])


def compute_delay(
    *,
    attempt_index: int,
    policy: BackoffPolicy,
) -> Tuple[float, bool]:
    """
    Compute the nominal delay (in seconds) and whether another retry
    is allowed under the given policy.

    Parameters
    ----------
    attempt_index:
        0-based index of the attempt.

        - attempt_index = 0 → first attempt (no previous failures)
        - attempt_index = 1 → first retry
        - attempt_index = 2 → second retry
        ...

    policy:
        BackoffPolicy to apply.

    Returns
    -------
    (delay_seconds, should_retry)

        delay_seconds:
            Suggested delay before this attempt (not before the next).

        should_retry:
            True if this attempt is allowed under max_retries,
            False if the caller should stop.

    Behavior
    --------
    - For attempt_index == 0: delay_seconds = 0.0, should_retry=True.
    - For attempt_index > policy.max_retries: should_retry=False
      and delay_seconds is still returned but should be ignored.
    """
    if attempt_index < 0:
        attempt_index = 0

    # Check retry allowance
    if attempt_index > policy.max_retries:
        # No more retries allowed
        return 0.0, False

    if attempt_index == 0:
        # First call: no delay before the attempt
        return 0.0, True

    # Retry attempts: exponential schedule
    retry_number = attempt_index  # 1, 2, 3, ...
    delay = policy.base_delay_seconds * (policy.multiplier ** (retry_number - 1))

    return float(delay), True


__all__ = [
    "BackoffProfile",
    "BackoffPolicy",
    "get_backoff_policy",
    "compute_delay",
]
