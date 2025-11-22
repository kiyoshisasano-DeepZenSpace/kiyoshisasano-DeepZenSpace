# Operational Categories (Draft)

---

## **Category 1: Runtime Drift Detection**

**Codes:**

* D0_none
* D1_instruction
* D2_context
* D3_repeated_plan
* D4_tool_error
* D5_latency_spike
* D5_information
* D9_unspecified
* D0_unspecified

**Triggers:**

* Instruction mismatch (D1)
* Format/Context deviation (D2)
* Repeated/looping plans (D3)
* Tool/API failure (D4)
* Latency anomaly or missing retrieval response (D5)
* Catch‑all or confidence fallback (D9, D0_unspecified)

**Associated Enforcement:**

* May lead to soft or hard repair depending on severity or recurrence.

**Risk Class:**

* Low → High depending on subtype (D0_none = benign, D4/D5 = high severity)

**Trace Evidence:**

* Found in runtime classifier and drift detection subsystem.

---

## **Category 2: Continue / Normal Execution**

**Codes:**

* C0_normal
* C0_user_turn
* C0_system_turn

**Triggers:**

* Normal execution with no detected drift; valid structured turn transition.

**Associated Enforcement:**

* Continue progression, no repair.

**Risk Class:**

* Lowest — validated healthy runtime state.

**Trace Evidence:**

* Logged in ingestion pipeline and runtime envelope notes.

---

## **Category 3: Repair Enforcement / Recovery Response**

**Codes:**

* R1_clarify
* R2_soft_repair
* R3_rewrite
* R4_request_clarification
* R5_hard_reset

**Triggers:**

* Initiated after a drift event; type and recurrence determine escalation.

**Associated Enforcement:**

* Clarify → Soft Repair → Rewrite → Explicit Request → Hard Reset

**Recoverability:**

* High for R1–R3; reduced for R4; system‑level reset for R5.

**Risk Class:**

* Escalates with repair level; R5 signals near‑failure.

**Trace Evidence:**

* Recorded via repair detector mapping.

---

## **Category 4: Terminal / Closure Outcome**

**Code:**

* O0_session_closed

**Trigger:**

* User exit or system/logic end state.

**Associated Enforcement:**

* Session termination; no continue or repair applicable.

**Risk Class:**

* Neutral unless prematurely invoked.

**Trace Evidence:**

* Ingestion layer final lifecycle marker.

---

## **Category 5: Observational Runtime Metrics (Non‑Intervention)**

**Codes:**

* PRDR
* VRL
* continue_repair_ratio
* failure_mode_clustering
* session_closure_typology

**Triggers:**

* Logging and analytics processes; not runtime-control linked.

**Associated Enforcement:**

* None — used for trend analysis, stability scoring, and anomaly tracking.

**Risk Class:**

* Not operational; monitoring only.

**Trace Evidence:**

* Analytics framework outputs.

---

## **UNSORTED**

* *(None — all provided codes mapped to operational categories based on runtime function and observed behavior)*
