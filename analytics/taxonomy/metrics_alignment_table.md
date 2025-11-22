# **Metrics Alignment Table (Initial Draft)**

Role: PLD v2 Observability/Analytics Layer Analyst  
Source: taxonomy\_observation\_sheet.csv  
Reference Specs: PLD\_metrics\_spec.md, event\_matrix.yaml

## **1\. Metrics Alignment Table**

| code | lifecycle\_phase | tentative\_metric\_category | measurable\_signal | notes | confidence (1-5) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **D0\_none** | Interaction (Loop) | **False Positive / Baseline** | Signal of system health checks returning negative for drift. (Silence verification) | Should likely be filtered out of "Incident" metrics but kept for "Health Check" volume. | 5 |
| **D1\_instruction** | Interaction (Loop) | **Accuracy (Intent)** | Signal that the agent's action diverged from user instruction. | Core quality metric. Critical for "Alignment" score. | 5 |
| **D2\_context** | Interaction (Loop) | **Data Integrity / Context** | Signal of schema violation or context window corruption. | Indicates pipeline fragility rather than model logic error. | 4 |
| **D3\_repeated\_plan** | Interaction (Loop) | **Efficiency (Stall)** | Signal of loop/stalemate where agent cannot progress. | High correlation with user frustration (churn risk). | 5 |
| **D4\_tool\_error** | Interaction (Loop) | **Reliability (dependency)** | Signal of downstream tool/API failure. | External dependency metric. Distinct from cognitive drift. | 5 |
| **D5\_latency\_spike** | Interaction (Loop) | **Performance (Latency)** | Signal of processing time exceeding QoS thresholds. | Purely operational metric. | 5 |
| **D5\_information** | Interaction (Loop) | **Accuracy (Retrieval)** | Signal of hallucination or failure to retrieve necessary knowledge. | **CONFLICT**: D5 is overloaded (Latency vs Info). See unresolved items. | 2 |
| **D9\_unspecified** | Interaction (Loop) | **Coverage (Unknown)** | Signal of unclassified anomaly. | High volume here indicates gap in taxonomy. | 4 |
| **D0\_unspecified** | Interaction (Loop) | **Data Quality (Ingestion)** | Signal of malformed event missing pld.code. | **CONFLICT**: D0 is overloaded (None vs Unspecified/Missing). | 3 |
| **C0\_normal** | Interaction (Loop) | **Throughput (Success)** | Signal of nominal progression. | Baseline for "Success Rate" denominator. | 5 |
| **C0\_user\_turn** | Interaction (Loop) | **Engagement (Input)** | Signal of user activity/input. | Used to normalize drift rates per turn. | 5 |
| **C0\_system\_turn** | Interaction (Loop) | **Engagement (Output)** | Signal of system response generation. |  | 5 |
| **O0\_session\_closed** | Resolution | **Completion Rate** | Signal of session termination. | Does not inherently imply success/failure without qualifier. | 4 |
| **R1\_clarify** | Recovery | **Intervention (Soft)** | Signal of agent seeking user guidance. | Low cost repair. | 5 |
| **R2\_soft\_repair** | Recovery | **Intervention (Auto)** | Signal of internal self-correction mechanism triggering. |  | 5 |
| **R3\_rewrite** | Recovery | **Intervention (Intensive)** | Signal of active plan rewriting. | Higher computational cost repair. | 5 |
| **R4\_request\_clarification** | Recovery | **Intervention (User-Loop)** | Signal of explicit delegation to user. | High friction repair. | 5 |
| **R5\_hard\_reset** | Recovery | **Intervention (Critical)** | Signal of state wipe/restart. | Indicates severe failure recovery. | 5 |
| **PRDR** | **Analysis (Post-Hoc)** | **Stability (Recurrence)** | Derived: Probability of drift $D\_x$ occurring after repair $R\_y$. | **Not a raw event**. Belongs to Analytics Layer, not Event Stream. | 5 |
| **VRL** | **Analysis (Post-Hoc)** | **Resilience (Time-to-Recover)** | Derived: Time delta $\\Delta t$ between Drift detection and Stable state. | **Not a raw event**. | 5 |
| **continue\_repair\_ratio** | **Analysis (Post-Hoc)** | **Stability Index** | Derived: Ratio $\\frac{\\sum C}{\\sum R}$. | **Not a raw event**. | 5 |
| **failure\_mode\_clustering** | **Analysis (Post-Hoc)** | **Defect Taxonomy** | Derived: Aggregate clusters of D-codes. | **Not a raw event**. | 5 |
| **session\_closure\_typology** | **Analysis (Post-Hoc)** | **Outcome Taxonomy** | Derived: Classification of $O\_0$ events context. | **Not a raw event**. | 5 |

## **2\. Unresolved Items & Conflicts**

### **A. Code Collision: D5**

* **Conflict**: D5 is currently assigned to both latency\_spike (Operational) and information (Cognitive/Retrieval).  
* **Reason**: Source files differ (pattern\_classifier.py vs drift\_detector.py) but the numeric code is identical. This creates aggregation errors in dashboards.  
* **Recommendation**: Reassign information to D6 or another unused integer.

### **B. Code Collision: D0**

* **Conflict**: D0 is none (clean state) and unspecified (missing code error).  
* **Reason**: One serves as a heartbeat (good), the other as an error handler (bad). Aggregating D0 will mix healthy signals with data quality errors.  
* **Recommendation**: Keep D0 as none (No Drift). Assign D99 or similar for missing\_code error handling.

### **C. Observational Rows in Taxonomy**

* **Ambiguity**: Rows like PRDR, VRL are listed alongside raw events but are clearly derived analytics metrics.  
* **Governance Question**: Should these have event codes (e.g., M\_prdr) and be emitted as summary events, or remain purely as documentation for SQL/Analytics views?

## **3\. Summary**

* **Alignment Confidence**: **85%**  
  * *High confidence in the core Drift/Repair flows, but lowered by the Code Collision issues which act as blockers for accurate measurement.*  
* **Major Ambiguity Clusters**:  
  1. **Overloaded Integers**: D0 and D5 are critically overloaded.  
  2. **Event vs. Metric Mixing**: The CSV mixes raw telemetry (events) with derived KPIs (PRDR, VRL).  
* **Recommendation for Next Governance Step**:  
  1. **IMMEDIATE**: Issue a patch to pld\_runtime to resolve D5 and D0 collisions.  
  2. **DECISION**: Define if PRDR/VRL are calculated *at runtime* (and thus need an event code like AnalyticsEvent) or *offline* (and should be removed from this taxonomy file).
