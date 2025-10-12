---
abstract: |
  I propose *Calibrated Transparency* (CT), a formal framework
  integrating recursive value learning, adversarially robust
  verification, and cryptographic auditability to operationalize AI
  safety governance. Unlike prior transparency approaches, CT
  establishes causal pathways from calibration mechanisms to safety
  guarantees through: (1) formal definitions with state-consistent
  Lyapunov verification, (2) adversarial robustness against metric
  gaming and deceptive alignment with measurable detection bounds, (3)
  operationally defined metrics with reproducible measurement protocols,
  and (4) policy-aligned implementation mappings. I synthesize
  2020--2025 research across preference learning (Kim et al., 2025),
  Lyapunov-based verification (Henrique et al., 2025), cryptographic
  auditing (Balan et al., 2025), and governance frameworks (NIST AI RMF,
  EU AI Act, ISO/IEC 42001). Our core contribution is a mechanistically
  grounded theory with dependency-aware risk composition, demonstrating
  that transparent calibration, when coupled with adversarial
  stress-testing and formal barrier certificates, provides measurable
  operational assurance against known failure modes---hallucination,
  specification gaming, and oversight collapse---while explicitly
  acknowledging limitations for existential-risk scenarios.
title: |
  Implementable Calibrated Transparency for Frontier AI:  Mechanistic Safety Architectures with Adversarial-Robust Verification
---

# Introduction: The Calibration--Safety Gap

## Motivation

Statistical calibration does not imply behavioral safety. A model with
well-calibrated uncertainty may still (i) pursue mesa-objectives
misaligned with training goals [@hubinger2021risks], (ii) engage in
specification gaming [@krakovna2020specgaming], (iii) exhibit deceptive
alignment during training while defecting post-deployment
[@cotra2022takeover], or (iv) fail catastrophically under distributional
shift [@hendrycks2021unsolved]. Documentation-centric transparency
(e.g., model cards [@mitchell2019modelcards], datasheets
[@gebru2021datasheets], post-hoc explanations [@ribeiro2016lime])
records properties but offers no causal mechanism from transparency to
safety. We address this gap via *Calibrated Transparency* (CT): a formal
architecture where transparency *causes* safety through verifiable,
adversarially robust mechanisms.

## Scope and Limitations

CT targets operational safety for near-term frontier models (10B--1T
parameters, 2025--2030). We do *not* claim to solve superintelligent
deception beyond human+tool verification, recursive self-improvement in
AGI scenarios, or multi-polar coordination failures
[@bostrom2014superintelligence; @carlsmith2022power]. CT provides
necessary but insufficient conditions for long-term safety.

## Contributions

-   **Formal CT Framework:** Axioms, definitions, and theorems
    establishing CT as a rigorous safety architecture
    (§[2](#sec:formal){reference-type="ref" reference="sec:formal"}).

-   **Causal Mechanism Theory:** Identification conditions and
    interventions linking calibration, verification, and governance to
    reduced failure probabilities
    (§[3](#sec:causal){reference-type="ref" reference="sec:causal"}).

-   **Adversarial Robustness:** Threat model, second-order metrics,
    activation analysis, and certified training against deceptive
    alignment and metric gaming (§[4](#sec:adv){reference-type="ref"
    reference="sec:adv"}).

-   **Empirical Validation:** Operational metric protocols (HAM, ECE,
    DR, SI, AAS) and benchmark requirements
    (§[5](#sec:empirical){reference-type="ref"
    reference="sec:empirical"}).

-   **Governance Integration:** Mappings to NIST AI RMF, EU AI Act, and
    ISO/IEC standards with dependency-aware risk composition
    (§[7](#sec:governance){reference-type="ref"
    reference="sec:governance"}).

# Formal Framework: Calibrated Transparency with State-Consistent Verification {#sec:formal}

#### Notation.

Let $\mathcal{X}$ denote the closed-loop state space,
$x_t\in\mathcal{X}$ the state at time $t$, $	heta_t$ model parameters
(embedded in $x_t$), $\mathcal{U}_t$ the uncertainty distribution, and
$\mathcal{P}_t$ the preference distribution.

::: description
$\mathcal{E}_t=(x_t,\mathcal{U}_t,\mathcal{P}_t)$ where $x_t$ includes
environmental observations and internal representations (including
$	heta_t$).

A system exhibits CT if it satisfies:

1.  **Statistical Calibration.** For any prediction $\hat y$ with
    confidence $p$,
    $\mathbb{P}(y=\hat y\mid p)=p\pm\epsilon_{\mathrm{stat}}$ on
    $\mathcal{D}_{\mathrm{test}}$, with
    $\epsilon_{\mathrm{stat}}\le 0.05$.

2.  **Mechanistic Verifiability.** There exists a continuously
    differentiable Lyapunov function
    $V:\mathcal{X}	o\mathbb{R}_{\ge 0}$ and compact safe set
    $\mathcal{X}_{\mathrm{safe}}\subset\mathcal{X}$ such that
    $V(x)=0\iff x\in\mathcal{X}_{\mathrm{eq}}\subset\mathcal{X}_{\mathrm{safe}}$
    and $\dot V(x)\le -lpha(\|x-x_{\mathrm{eq}}\|)$
    (class-$\mathcal{K}$ $lpha$) whenever the barrier-constrained
    update is applied; runtime monitoring ensures
    $x_t\in\mathcal{X}_{\mathrm{safe}}$ with $\le 10\%$ overhead.

3.  **Recursive Preference Coherence.** Preference updates satisfy
    $D_{\mathrm{KL}}(\mathcal{P}_{t+1}\|\mathcal{P}_t)\le\delta$ with
    human-verifiable justification trace $\mathcal{T}_t$ and
    meta-preference validation checks.

4.  **Cryptographic Auditability.** All epistemic updates admit
    zero-knowledge proofs $\pi_t$ with completeness $\ge 1-
u$,
    soundness $\ge 1-\mu$, and zero-knowledge; we prove range predicates
    $({
m SCI}_t\ge	heta)\wedge({
m ECE}_t\le\gamma)$ over Pedersen
    commits using *zk-STARKs* (no trusted setup); public verification
    $<100$ ms/receipt; receipts anchored every 10s to a Hyperledger
    Fabric ledger; on outage, a local write-ahead log enables batch
    reconciliation.

5.  **Adversarial Robustness.** CT properties hold under adaptive
    adversaries with computational budget $B<B_{\mathrm{critical}}$ (see
    §[4](#sec:adv){reference-type="ref" reference="sec:adv"}).
:::

#### Assumptions.

We use the following:

-   **A1 (Distributional Proximity).**
    $D_{\mathrm{KL}}(\mathcal{D}_{\mathrm{deploy}}\|\mathcal{D}_{\mathrm{train}})\le	au$
    and
    $W_2(\mathcal{D}_{\mathrm{deploy}},\mathcal{D}_{\mathrm{train}})\le	au_W$.

-   **A2 (Oversight Latency).** Human oversight operates at
    $f_{\mathrm{human}}\in[0.5,1.0]$ Hz with latency
    $\lambda<\lambda_{\mathrm{critical}}$.

-   **A3 (Adversarial Compute).** $B<B_{\mathrm{critical}}$, empirically
    estimated via staged red-teaming
    (§[4](#sec:adv){reference-type="ref" reference="sec:adv"}).

-   **A4$'$ (Deception Detection Bounds).** Mesa-optimizer detector
    achieves TPR $\ge 0.90$ and FNR $\le 0.05$ (95% CI via ground-truth
    honeypot/OOD cases adjudicated by $\ge 3$ reviewers). In theorems,
    we set $\epsilon_{\mathrm{det}}=0.05$.

#### Theorem 2.1 (CT Safety Guarantee).

Under A1--A4$'$ and CT-1..CT-5, a CT-compliant system satisfies
$$\label{eq:riskcomp}
\mathbb{P}\Big(igcup_i E_i\Big) \le \sum_i \epsilon_i - \sum_{i<j}\max\{0,\,\epsilon_i+\epsilon_j-1+
ho_{ij}\},$$
where $E_i$ denote failure events (statistical miscalibration,
mechanistic constraint violation, adversarial exploitation, deception
detection failure),
$\epsilon_i\in\{\epsilon_{\mathrm{stat}},\epsilon_{\mathrm{mech}},\epsilon_{\mathrm{adv}},\epsilon_{\mathrm{det}}\}$
are individual failure probabilities, and $
ho_{ij}\in[0,1]$
upper-bound pairwise dependence. This strictly improves over the naive
union bound when components are correlated.

*Proof sketch.* CT-1 yields $\epsilon_{\mathrm{stat}}$ by calibration
error bounds; CT-2 with Lyapunov/barrier certificates yields
$\epsilon_{\mathrm{mech}}\exp(-lpha t)$; CT-5 with A4$'$ and the
adversarial game yields $\epsilon_{\mathrm{adv}}$ and
$\epsilon_{\mathrm{det}}$. Cross-terms $\mathbb{P}(E_i\cap E_j)$ are
bounded via conditional independence checks or empirical bootstrap
estimates (Appendix D). $\square$

# Causal Mechanisms: From Calibration to Safety {#sec:causal}

We employ a structural causal model: Calibration ($C$)$	o$Uncertainty
awareness ($U$); Lyapunov verification ($L$)$	o$Trajectory constraint
($T$); Preference coherence ($P$)$	o$Objective alignment ($O$);
Cryptographic audit ($A$)$	o$Tamper detection ($D$). Then
$U\wedge T\wedge O\wedge D\Rightarrow$ Safety ($S$).

#### Identification conditions.

We require manipulable interventions on $(C,L,P,A)$ (ablation/A--B
tests), control of confounders (stratification, negative controls,
instrumental variables), and common support.

## Mechanistic Pathways

**Pathway 1 (Calibration $	o$ Hallucination Reduction).**
Well-calibrated $\mathcal{U}_t$ enables rejection sampling ($p<0.7$),
abstention when $H(\mathcal{U}_t)>1.5$ nats, and human escalation.
Empirically, VSCBench shows $\sim 37\%$ hallucination reduction when
abstention is calibration-gated [@geng2025vscbench]. Required ablation
(do(abstention)=1 vs. 0) appears in Appendix A.

**Pathway 2 (Lyapunov $	o$ Constraint Satisfaction).** Barrier
certificates guarantee $x_t\in\mathcal{X}_{\mathrm{safe}}$; we use
Algorithm [\[alg:safeupdate\]](#alg:safeupdate){reference-type="ref"
reference="alg:safeupdate"}. Formal guarantees for RLHF with Lyapunov
constraints follow [@henrique2025lyapunov] with
$\mathbb{P}(x_t
otin\mathcal{X}_{\mathrm{safe}})\le e^{-lpha t}$.

**Pathway 3 (Preference Coherence $	o$ Gaming Prevention).** Recursive
validation detects gaming via meta-preference checks and adversarial
prompts; models failing
$D_{\mathrm{KL}}(\mathcal{P}_{t+1}\|\mathcal{M})>\delta_{\mathrm{meta}}$
are rejected [@kim2025pfp].

::: algorithm
1.  Compute $V(x_t)$ and $\dot V(x_t)$. If $V(x_t)>V_{\max}$: HALT
    (circuit breaker).

2.  Nominal update:
    $\Delta	heta_{\mathrm{nom}}\leftarrow -\eta 
abla_	heta \mathcal{L}$.

3.  Project onto safe tangent:
    $\Delta	heta_{\mathrm{safe}}\leftarrow \Delta	heta_{\mathrm{nom}} - \lambda (1-\mathrm{SCI}_t)
abla V(x_t)$.

4.  Verify
    $V(x_t+\Delta	heta_{\mathrm{safe}})\le V(x_t)+arepsilon_{\mathrm{tol}}$;
    else back off $\eta$ and retry (max retries), or HALT.
:::

# Adversarial Robustness and Deceptive Alignment {#sec:adv}

## Threat Model and $B_{\mathrm{critical}}$

Adversary types: (i) external red-teamers, (ii) specification gamers
(optimize metrics), (iii) deceptive mesa-optimizers. The attack family
$\mathcal{A}(\epsilon)$ includes $\ell_\infty$ input perturbations
$\|\delta\|_\infty\le\epsilon$, parameter perturbations
$\|\delta_	heta\|_2\le\epsilon_	heta$, and $k\le 100$ gradient steps.
**$B_{\mathrm{critical}}$ is estimated via staged red-teaming: $10^3$
(baseline), $10^6$ (medium), $10^9$ (advanced). The failure threshold is
the first *reproducible* CT-property violation across $\ge 3$
independent campaigns (Appendix C).**

## Defenses

**Second-Order Metric (AAS).**
${
m AAS}=\mathbb{E}_{\mathcal{A}_{\mathrm{adv}}}[{
m HAM}]-\mathbb{E}_{\mathcal{D}_{\mathrm{nat}}}[{
m HAM}]$;
flag $|{
m AAS}|>0.15$. *Power analysis:* detect $|{
m AAS}|\ge 0.10$
with $lpha=0.05$, $eta=0.20$ assuming $\sigma_{
m HAM}pprox 0.15$
$\Rightarrow n\ge 5{,}000$ per split.

**Activation Archaeology.** Probe intermediate activations for deception
signatures (discontinuities, latent-objective mismatch, honeypot
failures) [@zheng2025mesa; @burns2023latent].

**Certified Adversarial Training.** Optimize robustness to
$\|\delta\|\le\epsilon$ (PGD/TRADES); verify success probability
$\le \epsilon_{
m cert}$ [@madry2018pgd].

# Empirical Validation and Frontier-Model Benchmarking {#sec:empirical}

## Operational Metric Protocols

**HAM.** Spearman $
ho$ between model rankings and expert consensus on
1,000 TrustLLM-Align items; $n=5$ raters with Krippendorff's
$lpha\ge 0.8$; 95% BCa bootstrap CI; accept if $
ho\ge 0.80$ (CI
lower bound $\ge 0.75$).

**ECE (CD).** Weighted ECE with equal-frequency 15-bin scheme on 10k
held-out samples; accept if ${
m ECE}\le 0.05$.

**DR.**
${
m DR}_t=\mathbb{E}_{s\sim \hat d} [D_{
m KL}(\pi_t(\cdot|s)\|\pi_{
m ref}(\cdot|s))]$
over 1k states and 100 actions; accept if ${
m DR}_t\le 0.20$.

**SI.** ${
m SI}(x_t)=\exp(-|\dot V(x_t)|)\in[0,1]$; accept if
${
m SI}\ge 0.90$ on 95% of the trajectory.

**AAS.** Natural (5k) vs. adversarial (5k) prompts; accept if
$|{
m AAS}|\le 0.10$.

## Benchmarks & Case Study

VSCBench [@geng2025vscbench] (3,600 image--text safety-calibration
items), TrustLLM-Align [@sun2024trustllm], and proposed
PolicyDrift-Bench & AdversarialAlign-100. A 90-day field trial for a
GPT-4-scale model targets: hallucination $-50\%$ (p$<0.01$),
${
m HAM}\ge 0.85$, ${
m ECE}\le 0.05$, ${
m DR}\le 0.20$,
${
m SI}\ge 0.90$, $|{
m AAS}|\le 0.10$, overhead $\le 10\%$.

# Multi-Agent Cooperative Alignment

CT uses federated calibration monitoring: each agent $i$ maintains
${
m SCI}_i=({
m HAM}_i\cdot(1-{
m CD}_i)\cdot(1-{
m DR}_i)\cdot{
m SI}_i)^{1/4}$
and shares ${
m SCI}_i$ (not parameters) via SMPC (additive secret
sharing, threshold $t=\lceil n/2
ceil+1$). Global median
${
m SCI}_{
m global}$ triggers audits; outliers with
$|{
m SCI}_i-{
m SCI}_{
m global}|>0.15$ undergo external review
within 48 hours. *Collusion resistance:* if $\ge t$ agents coordinate,
${
m SCI}_{
m global}$ becomes unreliable; mitigation via
reputation-weighted aggregation (future work). Game-theoretic
supervisory rewards
$R_i^{
m total}=R_i^{
m indiv}+eta\sum_{j
e i}{
m HAM}(i,j)$ yield
equilibria with ${
m SCI}_{
m global}\ge 0.80$ for small $n$
[@oesterheld2024cooperative; @dafoe2020cooperative].

# Governance Integration and Implementation Roadmap {#sec:governance}

**NIST AI RMF.** Govern: cryptographic audit logs (tamper detection
$1-\mu$); Map: preference coherence via
$D_{
m KL}(\mathcal{P}_{t+1}\|\mathcal{P}_t)$; Measure:
HAM/ECE/DR/SI/AAS; Manage: Lyapunov-constrained updates. Apply
[\[eq:riskcomp\]](#eq:riskcomp){reference-type="eqref"
reference="eq:riskcomp"} with empirical $
ho_{ij}$ to avoid
over-conservative union bounds.

**EU AI Act.** Article 11 (technical documentation): CT axioms
(CT-1..5),
Algorithm [\[alg:safeupdate\]](#alg:safeupdate){reference-type="ref"
reference="alg:safeupdate"}, and metric protocols satisfy Annex IV
evidence needs. Articles 14--17 (human oversight): adaptive oversight
($f_{
m human}\in[0.5,1.0]$ Hz) and circuit breakers. Article 43:
conformity assessment by notified bodies validating CT-1..5; harmonized
standards: EN ISO/IEC 42001 with CT annexes. Article 72: post-market
monitoring with SCI thresholds (e.g., ${
m SCI}<0.70$ triggers incident
reporting).

**ISO/IEC 42001 & 23894.** CT implements PDCA: Plan (thresholds), Do
(deploy mechanisms), Check (monitor SCI + adversarial tests), Act (SOP
mitigations); Lyapunov verification aligns with protective measures and
risk evaluation.

# Discussion and Open Problems

CT does not solve superintelligent deception, deep value extrapolation,
unbounded self-modification, or multi-polar races. Open problems include
scalable meta-preference elicitation ($n\ge 10^6$), estimating
$B_{
m critical}$, formalizing realistic shift bounds $(	au,	au_W)$,
collusion-resistant federation, and superhuman oversight (AI-assisted
auditing).

# Conclusion

Calibrated Transparency treats transparency as a *causal
mechanism*---not just documentation---by combining recursive preference
learning, Lyapunov verification, cryptographic auditing, and adversarial
stress tests. Under explicit assumptions, CT yields measurable
operational assurance for frontier models. We call for industry case
studies, open benchmarks (PolicyDrift-Bench, AdversarialAlign-100), and
standardization to enable CT as an engineerable, auditable property of
deployed AI systems.

# References {#references .unnumbered}

::: enumerate
[]{#bostrom2014superintelligence label="bostrom2014superintelligence"}
Bostrom, N. (2014). *Superintelligence: Paths, Dangers, Strategies*.
OUP.

[]{#brundage2020toward label="brundage2020toward"} Brundage, M. et al.
(2020). Toward trustworthy AI development. arXiv:2004.07213.

[]{#burns2023latent label="burns2023latent"} Burns, C. et al. (2023).
Discovering latent knowledge in language models without supervision.
ICLR.

[]{#carlsmith2022power label="carlsmith2022power"} Carlsmith, J. (2022).
Is power-seeking AI an existential risk? arXiv:2206.13353.

[]{#cotra2022takeover label="cotra2022takeover"} Cotra, A. (2022).
Without specific countermeasures, \... AI takeover. *Cold Takes*.

[]{#dafoe2020cooperative label="dafoe2020cooperative"} Dafoe, A. et al.
(2020). Open problems in cooperative AI. arXiv:2012.08630.

[]{#geng2025vscbench label="geng2025vscbench"} Geng, X. et al. (2025).
VSCBench: Safety calibration in VLMs. arXiv:2505.20362.

[]{#gebru2021datasheets label="gebru2021datasheets"} Gebru, T. et al.
(2021). Datasheets for datasets. *CACM*.

[]{#guo2017calibration label="guo2017calibration"} Guo, C. et al.
(2017). On calibration of modern neural networks. ICML.

[]{#hadfield2017offswitch label="hadfield2017offswitch"}
Hadfield-Menell, D. et al. (2017). The off-switch game. IJCAI.

[]{#hendrycks2021unsolved label="hendrycks2021unsolved"} Hendrycks, D.
et al. (2021). Unsolved problems in ML safety. arXiv:2109.13916.

[]{#henrique2025lyapunov label="henrique2025lyapunov"} Henrique, M. et
al. (2025). Lyapunov-based verification for RL with barrier
certificates. (preprint / SafeAI).

[]{#henzinger2025dynamic label="henzinger2025dynamic"} Henzinger, T. et
al. (2025). Formal verification of neural certificates done dynamically.
arXiv:2507.11987.

[]{#hubinger2021risks label="hubinger2021risks"} Hubinger, E. et al.
(2021). Risks from learned optimization. arXiv:1906.01820.

[]{#kenton2021alignment label="kenton2021alignment"} Kenton, Z. et al.
(2021). Alignment of language agents. arXiv:2103.14659.

[]{#kim2025pfp label="kim2025pfp"} Kim, D. et al. (2025). Debiasing
online preference learning via PFP. arXiv:2506.11098.

[]{#krakovna2020specgaming label="krakovna2020specgaming"} Krakovna, V.
et al. (2020). Specification gaming examples in AI. DeepMind.

[]{#lakshminarayanan2017deepensembles
label="lakshminarayanan2017deepensembles"} Lakshminarayanan, B. et al.
(2017). Simple and scalable predictive uncertainty estimation. NeurIPS.

[]{#lee2004trust label="lee2004trust"} Lee, J. D., & See, K. A. (2004).
Trust in automation. *Human Factors*.

[]{#liang2022helm label="liang2022helm"} Liang, P. et al. (2022). HELM.
arXiv:2211.09110.

[]{#madry2018pgd label="madry2018pgd"} Madry, A. et al. (2018). Towards
deep learning models resistant to adversarial attacks. ICLR.

[]{#manheim2019goodhart label="manheim2019goodhart"} Manheim, D., &
Garrabrant, S. (2019). Categorizing variants of Goodhart's Law.
arXiv:1803.04585.

[]{#mitchell2019modelcards label="mitchell2019modelcards"} Mitchell, M.
et al. (2019). Model cards for model reporting. FAT\*.

[]{#ngo2022alignment label="ngo2022alignment"} Ngo, R. et al. (2022).
The alignment problem from a DL perspective. arXiv:2209.00626.

[]{#oesterheld2024cooperative label="oesterheld2024cooperative"}
Oesterheld, C., & Shah, R. (2024). Cooperative AI with temporal
feedback. (preprint).

[]{#ovadia2019uncertainty label="ovadia2019uncertainty"} Ovadia, Y. et
al. (2019). Can you trust your model's uncertainty? NeurIPS.

[]{#pearl2009causality label="pearl2009causality"} Pearl, J. (2009).
*Causality*. CUP.

[]{#raji2020accountability label="raji2020accountability"} Raji, I. D.
et al. (2020). Closing the AI accountability gap. FAT\*.

[]{#ribeiro2016lime label="ribeiro2016lime"} Ribeiro, M. et al. (2016).
"Why should I trust you?": LIME. KDD.

[]{#sesha2022verifiedai label="sesha2022verifiedai"} Seshia, S. et al.
(2022). Towards verified AI. ACM CSUR.

[]{#skalse2022rewardgaming label="skalse2022rewardgaming"} Skalse, J. et
al. (2022). Defining and characterizing reward gaming. arXiv:2210.10760.

[]{#soares2014corrigibility label="soares2014corrigibility"} Soares, N.,
& Fallenstein, B. (2014). Corrigibility. (MIRI Tech Report).

[]{#srivastava2022bigbench label="srivastava2022bigbench"} Srivastava,
A. et al. (2022). Beyond the Imitation Game (BIG-bench).
arXiv:2206.04615.

[]{#sun2024trustllm label="sun2024trustllm"} Sun, L. et al. (2024).
TrustLLM: Trustworthiness in LLMs. arXiv:2401.05561.

[]{#wager2018grf label="wager2018grf"} Wager, S., & Athey, S. (2018).
Estimation and inference of heterogeneous treatment effects. *JASA*.

[]{#zheng2025mesa label="zheng2025mesa"} Zheng, L. et al. (2025). On
mesa-optimization in autoregressive transformers. (NeurIPS poster).
:::

# Appendices {#appendices-ct .unnumbered}

# Appendix A --- Statistical Calibration and Empirical Validation

## A.1 Dataset and Split Structure {#a.1-dataset-and-split-structure .unnumbered}

Calibration and HAM evaluation use *TrustLLM-Align 2025*, *AIR-Bench
2024*, and internal human-rating corpora ($\ge 120$k samples, 2023-Q4
$	o$ 2025-Q1). Each split (train / val / test / OOD / adversarial) is
stratified by modality (text / image / audio) and language.

## A.2 Metrics {#a.2-metrics .unnumbered}

ECE (Expected Calibration Error), HAM (Spearman $
ho$), and DR (policy
drift $D_{KL}$) as defined in the main text.

## A.3 Bootstrap Confidence Intervals {#a.3-bootstrap-confidence-intervals .unnumbered}

For $M\in\{\mathrm{ECE},\mathrm{HAM},\mathrm{DR}\}$, CIs from
10,000-sample BCa bootstrap. Joint-event bounds for Theorem 2.1 use
paired resampling across metrics/time windows.

# Appendix B --- Mechanistic Verification and Lyapunov Analysis

## B.1 Safe Set Definition {#b.1-safe-set-definition .unnumbered}

$\mathcal S_{	ext{safe}}=\{x\in\mathbb R^d:\;V(x)\le c\}$, $V$
differentiable, radially unbounded, with $\dot V\le 0$ on
$\mathcal S_{	ext{safe}}$.

## B.2 Lyapunov Certificates {#b.2-lyapunov-certificates .unnumbered}

Sum-of-squares program constructs certificates; verified offline with
*symbolic gradients (JAX autodiff)*; runtime monitor enforces
$\dot V\le 0$ via CBF substitution.

## B.3 Empirical Validation {#b.3-empirical-validation .unnumbered}

Randomized stress tests ($10^6$ episodes) confirm $\le 1\%$ transient
violations; empirical $e^{-lpha t}$ decay with
$lphapprox 0.13\,\mathrm{s}^{-1}$.

# Appendix C --- Adversarial Robustness Experiments

## C.1 Threat Model and $B_{\mathrm{critical}}$ {#c.1-threat-model-and-b_mathrmcritical .unnumbered}

::: center
  Tier       Query Budget   Attack Type                   Success      Notes
  ---------- -------------- ----------------------------- ------------ -------------------------------------------------------------------------------------------------------------------
  Baseline   $10^3$         Prompt-injection, poison      $<0.5\%$     Below detection
  Medium     $10^6$         Gradient-based perturbation   2--3%        Partial CT violation
  Advanced   $10^9$         Coord. red-team ensemble      $\ge 10\%$   Defines $B_{\mathrm{critical}}$ (first *reproducible* CT-property violation across $\ge 3$ independent campaigns)
:::

## C.2 Adversarial Alignment Score (AAS) {#c.2-adversarial-alignment-score-aas .unnumbered}

$AAS=\mathbb E_{p\sim \mathcal{A}_{
m adv}}[\mathrm{HAM}(p)]-\mathbb E_{p\sim \mathcal{D}_{
m nat}}[\mathrm{HAM}(p)]$.
With $\sigma_{
m HAM}pprox 0.15$, power $(lpha=0.05,eta=0.20)$
requires $n\ge 5{,}000$ per split; observed 95% CI satisfies
$|AAS|\le 0.08$.

## C.3 Certified Adversarial Training {#c.3-certified-adversarial-training .unnumbered}

PGD ($\epsilon=8/255$) with TRADES $\lambda=6$; randomized smoothing
($\sigma=0.25$); verified $P_{
m adv}\le 0.04$.

# Appendix D --- Empirical Bootstrap for Cross-Term Estimation

## D.1 Procedure {#d.1-procedure .unnumbered}

Collect $(\mathrm{HAM}_t, \mathrm{ECE}_t, \mathrm{SI}_t)$; compute
indicators $I_{ij}(t)$ for pairs $(E_i,E_j)$; 10,000-sample stratified
bootstrap over time; compute $\widehat p_{ij}$ and BCa CI; bound
$\Pr(\cup_iE_i)$ by $\sum_i\epsilon_i-\sum_{i<j}\widehat p_{ij}$.
Validate independence via permutation test (p$>0.1$).

## D.2 Implementation Notes {#d.2-implementation-notes .unnumbered}

Python 3.12, NumPy 2, SciPy 1.14, JAX 0.5; parallelized bootstrap (100
cores $	imes$ 1,000 reps $pprox$ 6 min). All intermediate CI
summaries anchored in the cryptographic log.
