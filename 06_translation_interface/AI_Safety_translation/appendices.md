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
$\to$ 2025-Q1). Each split (train / val / test / OOD / adversarial) is
stratified by modality (text / image / audio) and language.

## A.2 Metrics {#a.2-metrics .unnumbered}

ECE (Expected Calibration Error), HAM (Spearman $\rho$), and DR (policy
drift $D_{KL}$) as defined in the main text.

## A.3 Bootstrap Confidence Intervals {#a.3-bootstrap-confidence-intervals .unnumbered}

For $M\in\{\mathrm{ECE},\mathrm{HAM},\mathrm{DR}\}$, CIs from
10,000-sample BCa bootstrap. Joint-event bounds for Theorem 2.1 use
paired resampling across metrics/time windows.

# Appendix B --- Mechanistic Verification and Lyapunov Analysis

## B.1 Safe Set Definition {#b.1-safe-set-definition .unnumbered}

$\mathcal S_{\text{safe}}=\{x\in\mathbb R^d:\;V(x)\le c\}$, $V$
differentiable, radially unbounded, with $\dot V\le 0$ on
$\mathcal S_{\text{safe}}$.

## B.2 Lyapunov Certificates {#b.2-lyapunov-certificates .unnumbered}

Sum-of-squares program constructs certificates; verified offline with
*symbolic gradients (JAX autodiff)*; runtime monitor enforces
$\dot V\le 0$ via CBF substitution.

## B.3 Empirical Validation {#b.3-empirical-validation .unnumbered}

Randomized stress tests ($10^6$ episodes) confirm $\le 1\%$ transient
violations; empirical $e^{-\alpha t}$ decay with
$\alpha\approx 0.13\,\mathrm{s}^{-1}$.

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

$AAS=\mathbb E_{p\sim \mathcal{A}_{\rm adv}}[\mathrm{HAM}(p)]-\mathbb E_{p\sim \mathcal{D}_{\rm nat}}[\mathrm{HAM}(p)]$.
With $\sigma_{\rm HAM}\approx 0.15$, power $(\alpha=0.05,\beta=0.20)$
requires $n\ge 5{,}000$ per split; observed 95% CI satisfies
$|AAS|\le 0.08$.

## C.3 Certified Adversarial Training {#c.3-certified-adversarial-training .unnumbered}

PGD ($\epsilon=8/255$) with TRADES $\lambda=6$; randomized smoothing
($\sigma=0.25$); verified $P_{\rm adv}\le 0.04$.

# Appendix D --- Empirical Bootstrap for Cross-Term Estimation

## D.1 Procedure {#d.1-procedure .unnumbered}

Collect $(\mathrm{HAM}_t, \mathrm{ECE}_t, \mathrm{SI}_t)$; compute
indicators $I_{ij}(t)$ for pairs $(E_i,E_j)$; 10,000-sample stratified
bootstrap over time; compute $\widehat p_{ij}$ and BCa CI; bound
$\Pr(\cup_iE_i)$ by $\sum_i\epsilon_i-\sum_{i<j}\widehat p_{ij}$.
Validate independence via permutation test (p$>0.1$).

## D.2 Implementation Notes {#d.2-implementation-notes .unnumbered}

Python 3.12, NumPy 2, SciPy 1.14, JAX 0.5; parallelized bootstrap (100
cores $\times$ 1,000 reps $\approx$ 6 min). All intermediate CI
summaries anchored in the cryptographic log.
