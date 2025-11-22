# Semantic Taxonomy (Preliminary Clustering)

## Cluster 1: Drift Detection Signals
- **Applicable Codes**: `D0_none`, `D1_instruction`, `D2_context`, `D3_repeated_plan`, `D4_tool_error`, `D5_latency_spike`, `D5_information`, `D9_unspecified`, `D0_unspecified`
- **Shared Characteristics**: Runtime detection of deviation from expected behavior patterns
- **Target Domain**: drift detection, anomaly classification, performance degradation monitoring
- **Supporting Evidence**: All sourced from `pattern_classifier.py` and `drift_detector.py`, lifecycle_phase="drift", event_type="drift_detected"
- **Confidence Level**: 5

### Subcluster 1.1: Content/Intent Drifts
- **Applicable Codes**: `D1_instruction`, `D2_context`, `D5_information`
- **Characteristics**: Semantic or informational misalignment
- **Confidence Level**: 4

### Subcluster 1.2: Behavioral/Pattern Drifts
- **Applicable Codes**: `D3_repeated_plan`, `D4_tool_error`, `D5_latency_spike`
- **Characteristics**: Execution or performance anomalies
- **Confidence Level**: 4

### Subcluster 1.3: Default/Fallback Classifications
- **Applicable Codes**: `D0_none`, `D0_unspecified`, `D9_unspecified`
- **Characteristics**: Baseline or unclassified drift states
- **Confidence Level**: 5

## Cluster 2: Session Flow Control
- **Applicable Codes**: `C0_normal`, `C0_user_turn`, `C0_system_turn`
- **Shared Characteristics**: Normal conversation flow continuation markers
- **Target Domain**: conversation management, turn-taking control, dialog state tracking
- **Supporting Evidence**: lifecycle_phase="continue", event_type="continue_allowed", primarily from MultiWOZ adapter
- **Confidence Level**: 5

## Cluster 3: Repair Interventions (Escalation Hierarchy)
- **Applicable Codes**: `R1_clarify`, `R2_soft_repair`, `R3_rewrite`, `R4_request_clarification`, `R5_hard_reset`
- **Shared Characteristics**: Progressive escalation of corrective actions (R1→R5 indicates severity)
- **Target Domain**: error recovery, conversation repair, drift mitigation
- **Supporting Evidence**: All from `repair_detector.py`, lifecycle_phase="repair", event_type="repair_triggered"
- **Confidence Level**: 5

### Repair Escalation Pattern:
1. **Minimal**: `R1_clarify` - lightweight adjustment
2. **Moderate**: `R2_soft_repair` - default/fallback repair
3. **Significant**: `R3_rewrite` - content regeneration
4. **Interactive**: `R4_request_clarification` - user engagement
5. **Maximum**: `R5_hard_reset` - complete restart

## Cluster 4: Session Termination
- **Applicable Codes**: `O0_session_closed`
- **Shared Characteristics**: Session lifecycle completion marker
- **Target Domain**: session management, resource cleanup, state finalization
- **Supporting Evidence**: lifecycle_phase="outcome", event_type="session_closed"
- **Confidence Level**: 5

## Cluster 5: Analytics & Observational Metrics
- **Applicable Codes**: `PRDR`, `VRL`, `continue_repair_ratio`, `failure_mode_clustering`, `session_closure_typology`
- **Shared Characteristics**: Post-hoc analytical frameworks, not runtime codes
- **Target Domain**: system health monitoring, performance analysis, failure pattern recognition
- **Supporting Evidence**: normative_level="observational", located in analytics/ directory
- **Confidence Level**: 5

### Subcluster 5.1: Recovery Metrics
- **Applicable Codes**: `PRDR`, `VRL`
- **Characteristics**: Measure repair effectiveness and timing

### Subcluster 5.2: Pattern Analysis
- **Applicable Codes**: `failure_mode_clustering`, `session_closure_typology`
- **Characteristics**: Aggregate behavior classification

### Subcluster 5.3: Stability Indicators
- **Applicable Codes**: `continue_repair_ratio`
- **Characteristics**: System stability measurement

## UNRESOLVED
- **Ambiguity Note**: `D5` has dual assignment (`D5_latency_spike` and `D5_information`) with different descriptors but same numeric code
  - **Confidence Level**: 2 (unclear if intentional overloading or versioning artifact)
  - **Recommendation**: Verify if this represents evolution of D5 usage or concurrent dual-purpose coding

## Cross-Cluster Observations
1. **Lifecycle Flow**: D (detect) → R (repair) → C (continue) or O (outcome)
2. **Numeric Pattern**: Lower numbers (0-1) often indicate baseline/normal states
3. **Source Concentration**: Most runtime codes originate from 3-4 core detection/classification modules
4. **Normative Levels**: Clear separation between runtime operational codes and observational analytics

## Summary Statistics
- **Total Codes Analyzed**: 24
- **Primary Clusters**: 5
- **Unresolved Items**: 1 (D5 dual assignment)
- **Confidence Distribution**:
  - Level 5 (Highest): 4 clusters
  - Level 4 (High): 2 subclusters
  - Level 2 (Low): 1 ambiguity

## Semantic Structure Visualization

```
PLD v2 Code Space
├── Runtime Codes (normative_level="runtime")
│   ├── D-prefix (Drift Detection)
│   │   ├── Content Drifts (D1, D2, D5_information)
│   │   ├── Behavioral Drifts (D3, D4, D5_latency)
│   │   └── Defaults (D0, D9)
│   ├── R-prefix (Repair Actions)
│   │   └── Escalation: R1 → R2 → R3 → R4 → R5
│   ├── C-prefix (Continue Flow)
│   │   └── Turn Management (C0 variants)
│   └── O-prefix (Outcomes)
│       └── Session Closure (O0)
└── Observational Codes (normative_level="observational")
    ├── Recovery Metrics (PRDR, VRL)
    ├── Pattern Analysis (failure_mode_clustering, session_closure_typology)
    └── Stability Indicators (continue_repair_ratio)
```

## Key Insights
1. **Clear Lifecycle Model**: The codes follow a state machine pattern with drift detection triggering repairs, leading to either continuation or session outcomes
2. **Escalation Semantics**: Numeric suffixes in R-codes directly map to intervention severity
3. **Dual-Purpose Prefixes**: Some prefixes (especially D and C) serve both specific event classification and default/fallback roles
4. **Analytics Separation**: Observational metrics are clearly separated from runtime operational codes

**Overall Taxonomy Confidence**: 4/5
- Strong evidence for primary clusters
- Clear escalation patterns in repair codes
- Ambiguity only in D5 dual assignment
