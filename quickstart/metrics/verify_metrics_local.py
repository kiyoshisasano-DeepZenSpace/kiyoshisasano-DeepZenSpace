# quickstart/metrics/verify_metrics_local.py
#
# Purpose:
#   Minimal local script to demonstrate how to calculate PLD Operational Metrics
#   using DuckDB, based on `pld_event.schema.json` and a demo dataset.
#
#   This is a companion to:
#     docs/07_pld_operational_metrics_cookbook.md
#
# Requirements:
#   - duckdb Python package (`pip install duckdb`)
#   - quickstart/metrics/datasets/pld_events_demo.jsonl (demo data; see docs for schema)
#
# Usage:
#   python3 quickstart/metrics/verify_metrics_local.py

import os
import sys


def main() -> None:
    print("--- PLD Local Metrics Verification Script ---")

    # 1. Check for DuckDB installation
    try:
        import duckdb  # type: ignore
    except ImportError:
        print("❌ DuckDB Python package not found.")
        print("   Please install it: `pip install duckdb`")
        sys.exit(1)

    # 2. Check for the demo dataset
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, "datasets", "pld_events_demo.jsonl")

    if not os.path.exists(data_path):
        print(f"❌ Demo dataset not found at: {data_path}")
        print("   Please ensure `pld_events_demo.jsonl` exists in the `datasets/` folder.")
        sys.exit(1)

    # 3. Connect to DuckDB (in-memory)
    con = duckdb.connect(database=":memory:", read_only=False)
    print(f"✅ DuckDB connected. Loading data from: {data_path}")

    # 4. Load JSONL data into a DuckDB table
    try:
        con.execute(
            f"""
            CREATE TABLE pld_events AS
            SELECT * FROM read_json_auto('{data_path}');
            """
        )
        print("✅ Data loaded into table: pld_events")
    except Exception as e:
        print(f"❌ Failed to load data into DuckDB: {e}")
        sys.exit(1)

    print("\n--- Calculating PLD Metrics (per docs/07_pld_operational_metrics_cookbook.md) ---")

    # -------------------------------------------------------------------------
    # Metric 1 — Post-Repair Drift Recurrence (PRDR)
    # -------------------------------------------------------------------------
    print("\n--- Metric 1: Post-Repair Drift Recurrence (PRDR) ---")

    # N = 5 turns (demo) — see cookbook for rationale
    prdr_query = """
    WITH repairs AS (
        SELECT
            session_id,
            turn_index AS repair_turn
        FROM pld_events
        WHERE event_type = 'repair'
    ),
    drift_after AS (
        SELECT
            r.session_id,
            r.repair_turn,
            COUNT(*) AS drift_count
        FROM repairs r
        JOIN pld_events e
          ON e.session_id = r.session_id
         AND e.turn_index BETWEEN r.repair_turn + 1 AND r.repair_turn + 5
         AND e.event_type = 'drift'
        GROUP BY r.session_id, r.repair_turn
    )
    SELECT
        COALESCE(
            SUM(COALESCE(drift_count, 0)) * 1.0
            / NULLIF(COUNT(*), 0),
            0.0
        ) AS prdr_score
    FROM repairs r
    LEFT JOIN drift_after d
      ON r.session_id = d.session_id
     AND r.repair_turn = d.repair_turn;
    """

    prdr_result = con.execute(prdr_query).fetchone()
    prdr_value = prdr_result[0]
    print(f"PRDR (Post-Repair Drift Recurrence): {prdr_value:.3f}")

    # Simple interpretation (aligned with cookbook ranges)
    if prdr_value <= 0.10:
        print("   ✅ Interpretation: Repairs are generally holding (0–10%).")
    elif prdr_value <= 0.30:
        print("   ⚠️  Interpretation: Repairs partially effective (10–30%).")
    else:
        print("   ❌ Interpretation: Repairs fragile / repetitive (>30%).")

    # -------------------------------------------------------------------------
    # Metric 2 — Repair Efficiency Index (REI)
    # -------------------------------------------------------------------------
    print("\n--- Metric 2: Repair Efficiency Index (REI) ---")
    print("REI = (improvement in task success rate) / (average cost per session)")
    print("This metric requires A/B-style data with baseline vs with-repairs cohorts.")
    print("It is not calculated from this demo dataset.\n"
          "See docs/07_pld_operational_metrics_cookbook.md for implementation guidance.\n")

    # -------------------------------------------------------------------------
    # Metric 3 — Visible Repair Load (VRL)
    # -------------------------------------------------------------------------
    print("\n--- Metric 3: Visible Repair Load (VRL) ---")

    # Mapping to event_type is aligned with the cookbook:
    #   - repair_visible
    #   - clarification_prompt
    vrl_query = """
    SELECT
        COALESCE(
            (COUNT(*) FILTER (
                WHERE event_type IN ('repair_visible', 'clarification_prompt')
            ) * 100.0)
            / NULLIF(COUNT(DISTINCT session_id || '-' || turn_index), 0),
            0.0
        ) AS vrl_score
    FROM pld_events;
    """

    vrl_result = con.execute(vrl_query).fetchone()
    vrl_value = vrl_result[0]
    print(f"VRL (Visible Repair Load): {vrl_value:.3f} per 100 turns")

    # -------------------------------------------------------------------------
    # Metric 4 — Failover Rate (FR)
    # -------------------------------------------------------------------------
    print("\n--- Metric 4: Failover Rate (FR) ---")

    fr_query = """
    SELECT
        COALESCE(
            (COUNT(DISTINCT CASE WHEN event_type = 'failover' THEN session_id END) * 100.0)
            / NULLIF(COUNT(DISTINCT session_id), 0),
            0.0
        ) AS fr_score
    FROM pld_events;
    """

    fr_result = con.execute(fr_query).fetchone()
    fr_value = fr_result[0]
    print(f"FR (Failover Rate): {fr_value:.3f}%")

    # -------------------------------------------------------------------------
    # Metric 5 — Mean Repairs Before Failover (MRBF)
    # -------------------------------------------------------------------------
    print("\n--- Metric 5: Mean Repairs Before Failover (MRBF) ---")

    # Count repair events that occur *before* the first failover in each session.
    # This avoids requiring a dedicated `repair_attempt_id` column.
    mrbf_query = """
    WITH failover_turn AS (
        SELECT
            session_id,
            MIN(turn_index) AS failover_turn
        FROM pld_events
        WHERE event_type = 'failover'
        GROUP BY session_id
    ),
    repairs_before_failover AS (
        SELECT
            f.session_id,
            COUNT(*) AS repair_attempts
        FROM failover_turn f
        JOIN pld_events e
          ON e.session_id = f.session_id
         AND e.event_type = 'repair'
         AND e.turn_index < f.failover_turn
        GROUP BY f.session_id
    )
    SELECT
        COALESCE(
            SUM(repair_attempts) * 1.0 / NULLIF(COUNT(*), 0),
            0.0
        ) AS mrbf_score
    FROM repairs_before_failover;
    """

    mrbf_result = con.execute(mrbf_query).fetchone()
    mrbf_value = mrbf_result[0]
    print(f"MRBF (Mean Repairs Before Failover): {mrbf_value:.3f}")

    print("\n--- Metrics Calculation Complete ---")
    con.close()


if __name__ == "__main__":
    main()
