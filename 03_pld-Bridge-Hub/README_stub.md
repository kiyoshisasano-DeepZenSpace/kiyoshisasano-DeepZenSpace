# 🧠 PLD-Bridge Hub

The **PLD-Bridge Hub** acts as the integration layer between theoretical models from **01_phase_loop_dynamics** and practical implementations in **02_quickstart_kit**.

It enables consistent event generation, metric aggregation, and UI pattern deployment across different PLD-driven systems.

---

## 🚀 Purpose

Bridge Hub provides:

1. **Schema Alignment**  
   Uses the validated schemas from `02_quickstart_kit/30_metrics/schemas/metrics_schema.yaml` and `pld_event.schema.json`  
   → Ensures event logs are structurally consistent and validator-ready.

2. **Metric & Event Processing**  
   Aggregates telemetry according to shared definitions: drift, repair, reentry, latency_hold.

3. **Pattern-Linked UI Logic**  
   Implements interaction patterns (`reentry`, `soft_repair`, `latency_hold`) in the Bridge Hub front-end, aligned with metrics.

---

## 📂 Structure

- `/event_emitters/` — Event generation code (schema-compliant)
- `/aggregators/` — Metric aggregation & reporting scripts
- `/ui_patterns/` — Front-end integrations (React / Figma prototypes)
- `/docs/` — Implementation notes & validator usage

---

## 📊 Core Schemas

**Event Schema:**  
[`pld_event.schema.json`](../02_quickstart_kit/30_metrics/schemas/pld_event.schema.json)  
- Validates event types and metadata  
- `latency_hold` requires `duration_ms` (milliseconds)

**Metrics Schema:**  
[`metrics_schema.yaml`](../02_quickstart_kit/30_metrics/schemas/metrics_schema.yaml)  
- Defines available events and metrics formulas  
- Ensures uniform tracking across LLM, Rasa, and UI

---

## 🔄 Revision Background

This version reflects the August 2025 **Quickstart Kit alignment update**:

- Updated to match `metrics_schema.yaml` (added field descriptions, naming consistency)
- `pld_event.schema.json` changes: latency_hold events now require `duration_ms`
- Demo data & validator instructions available in `02_quickstart_kit/README_quickstart.md`

---

## 📜 License

Distributed under **CC BY-NC 4.0**.  
See usage guidelines in [`PLD_OVERVIEW.md`](./PLD_OVERVIEW.md).
