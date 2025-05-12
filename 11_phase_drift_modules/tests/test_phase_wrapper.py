# test_phase_wrapper.py

import pytest
import asyncio
import os
import json
import time
from phase_wrapper import phase_wrap

LOG_FILE = "phase_drift_log.json"


# Utility: Remove log file before test
@pytest.fixture(autouse=True)
def clean_log():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    yield
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)


def read_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE) as f:
        return [json.loads(line.strip()) for line in f if line.strip()]


# Synchronous example
@phase_wrap(delay_range=(0.1, 0.2), timeout=1.0, fallback_message="fallback-sync")
def sync_function(success=True):
    if success:
        time.sleep(0.1)
        return "ok-sync"
    else:
        time.sleep(2)  # Will cause fallback
        return "too slow"


# Asynchronous example
@phase_wrap(delay_range=(0.1, 0.2), timeout=1.0, fallback_message="fallback-async")
async def async_function(success=True):
    if success:
        await asyncio.sleep(0.1)
        return "ok-async"
    else:
        await asyncio.sleep(2)  # Will timeout
        return "too slow"


def test_sync_passes():
    result = sync_function(success=True)
    assert result == "ok-sync"
    logs = read_log()
    assert len(logs) == 1
    assert logs[0]["silence_used"] is False


def test_sync_fallback():
    result = sync_function(success=False)
    assert result == "fallback-sync"
    logs = read_log()
    assert len(logs) == 1
    assert logs[0]["silence_used"] is True


@pytest.mark.asyncio
async def test_async_passes():
    result = await async_function(success=True)
    assert result == "ok-async"
    logs = read_log()
    assert len(logs) == 1
    assert logs[0]["silence_used"] is False


@pytest.mark.asyncio
async def test_async_timeout_fallback():
    result = await async_function(success=False)
    assert result == "fallback-async"
    logs = read_log()
    assert len(logs) == 1
    assert logs[0]["silence_used"] is True
