# ML-for-Security Pitfalls Audit Guide

Based on "Pitfalls in Machine Learning for Computer Security" (Arp et al., CACM 2024 / USENIX Security 2022). This paper analyzed 30 top-tier security conference papers and found every paper suffered from at least 3 pitfalls. Use this as a systematic audit checklist.

---

## The 10 Pitfalls: Audit Checklist

For each pitfall, assess: **Clean** (not present), **Partially Present** (acknowledged/mitigated), **Present** (unaddressed), **Unclear** (cannot determine from text).

---

### P1: Sampling Bias (90% prevalence in literature)

**Definition**: Collected data does not sufficiently represent the true data distribution.

**What to check**:
- Is the attack-to-benign ratio in the dataset stated?
- Does this ratio match real-world deployment scenarios?
- Are multiple data sources combined? If so, is source-specific bias discussed?
- Is the training set drawn from the same distribution as the intended deployment?
- Are there temporal biases (all attacks from one time period, all benign from another)?

**Security-specific concerns**:
- APT attacks are extremely rare in production (<<0.1% of traffic)
- Lab datasets often have unrealistically high attack ratios (10-50%)
- Attack diversity: are multiple TTPs represented, or just one attack campaign?
- Benign diversity: does benign traffic cover diverse applications/protocols?

**Questions to ask the paper**:
- "What is the attack prevalence in your datasets, and how does it compare to real-world environments?"
- "How would performance change if the attack ratio were 0.01% instead of X%?"

---

### P2: Label Inaccuracy (10% prevalence)

**Definition**: Ground-truth labels are inaccurate, unstable, or erroneous.

**What to check**:
- How were labels obtained? (manual annotation, heuristic, automated tool)
- Is the labeling methodology described?
- Are there known labeling issues in the used datasets?
- Is label noise discussed?

**Security-specific concerns**:
- VirusTotal consensus labels are noisy and time-varying
- CIC-series datasets have documented labeling errors
- DARPA datasets: labels are relatively clean (controlled experiments) but synthetic
- Real-world labels: often incomplete (only known attacks labeled, unknown attacks missed)

---

### P3: Data Snooping (73% prevalence)

**Definition**: Model is trained with data not typically available in practice.

**Three forms of data snooping**:

1. **Temporal snooping**: Future information leaks into training
   - Check: Is the data split temporal? Or random (potentially mixing future and past)?
   - Check: Are features that encode absolute time properly handled?
   - Check: Does feature normalization use full-dataset statistics?

2. **In-sample snooping**: Test data influences training
   - Check: Are normalization parameters computed on training set only?
   - Check: Is feature selection/engineering done before or after splitting?
   - Check: Is hyperparameter tuning done on a held-out validation set?

3. **Leakage through auxiliary data**: External information not available at deployment
   - Check: Are features used that require knowledge of the full graph/dataset?
   - Check: Do graph-based features (centrality, PageRank) use test-time edges?

**High-risk for graph-based methods**: Graph construction that uses all nodes (including test) to compute structural features → information from test nodes leaks into training.

---

### P4: Spurious Correlations (20% prevalence)

**Definition**: Model learns artifacts unrelated to the security problem.

**What to check**:
- Is there feature importance analysis?
- Are there known confounders in the data? (e.g., all attacks from one IP range)
- Has the model been tested for sensitivity to non-security features?
- Is there an explainability analysis (SHAP, attention visualization)?

**Common confounders in security data**:
- IP address ranges correlating with attack/benign labels
- Time-of-day patterns (attacks launched at specific hours in lab)
- Protocol distribution artifacts (all attacks use TCP, all benign includes UDP)
- Dataset-specific artifacts (specific tools or configurations unique to one dataset)

**Questions to ask**:
- "What features contribute most to predictions? Are they security-relevant?"
- "Would the model still work if IP addresses were randomized?"

---

### P5: Biased Parameter Selection (10% prevalence)

**Definition**: Final parameters are not entirely fixed at training time; they depend on test data.

**What to check**:
- Is the detection threshold chosen on the validation set or test set?
- Is the "best model" selected based on test set performance?
- Are hyperparameters tuned on a separate validation set?
- Is the tuning procedure fully described?

**Key distinction**:
- Reporting AUC/AUPRC (threshold-free) is less susceptible
- Reporting F1/Precision/Recall (threshold-dependent) requires specifying how threshold was chosen

---

### P6: Inappropriate Baselines (20% prevalence)

**Definition**: Evaluation without sufficient or appropriate baseline methods.

**What to check**:
- Are baselines from the same year or recent? (not all 5+ years old)
- Do baselines include both ML and non-ML approaches?
- Do baselines include simple/traditional methods (to show ML adds value)?
- Are baselines from the same problem domain?
- Is a simple baseline included (e.g., Random Forest on same features)?
- Are baselines fairly configured (original hyperparameters)?

**Checklist for security papers**:
- [ ] At least 1 traditional ML baseline (RF, SVM, XGBoost)
- [ ] At least 1 domain-specific baseline (security-focused method)
- [ ] At least 1 recent baseline (published within 2 years)
- [ ] At least 1 simple baseline (to show problem isn't trivially solvable)

---

### P7: Inappropriate Performance Measures (33% prevalence)

**Definition**: Chosen metrics don't account for application constraints.

**For security detection tasks**:

| Situation | Appropriate Metrics | Inappropriate Metrics |
|-----------|-------------------|-----------------------|
| Extreme class imbalance (>100:1) | AUPRC, F1, Precision@Recall | Accuracy, AUROC (can be misleading) |
| Operational deployment focus | FPR@TPR=0.95, detection latency | Only AUROC (hides threshold choice) |
| Ranking/prioritization | AUROC, NDCG | Only Precision/Recall |

**Must-report for detection papers**:
- Precision and Recall (not just F1)
- False Positive Rate at operationally relevant True Positive Rates
- AUPRC for imbalanced settings

---

### P8: Base Rate Fallacy (10% prevalence)

**Definition**: Class imbalance ignored when interpreting performance.

**The problem**: A 1% FPR sounds low, but with 0.01% attack prevalence:
- For every 10,000 flows: ~1 true attack, ~100 false alarms
- Precision = 1/101 ≈ 1%
- The analyst drowns in false positives

**What to check**:
- Is the base rate (attack prevalence) of the deployment scenario stated?
- Are absolute numbers of false positives computed?
- Is the precision at realistic base rates calculated?
- Is the operational burden of false positives discussed?

**Formula**: `Precision_real = (TPR × base_rate) / (TPR × base_rate + FPR × (1 - base_rate))`

---

### P9: Lab-Only Evaluation (47% prevalence)

**Definition**: System evaluated only in laboratory setting without discussing practical limitations.

**What to check**:
- Is there discussion of deployment-to-lab gap?
- Are practical limitations explicitly stated?
- Is concept drift (performance degradation over time) discussed?
- Is the system tested on any real-world or production-like data?
- Is computational cost at production scale estimated?

**For graph-based security methods**:
- How does graph size scale in production vs. lab?
- What is the graph construction latency in streaming scenarios?
- How is the system maintained/updated with new data?

---

### P10: Inappropriate Threat Model (17% prevalence)

**Definition**: Security of the ML system itself is not considered.

**What to check**:
- Is adversarial robustness discussed?
- Can the attacker observe and adapt to the detector?
- Is evasion cost analyzed (how much effort to bypass)?
- Is the model susceptible to data poisoning?
- Are there features an attacker can easily manipulate?

---

## §IDS: Extra Pitfalls for Intrusion Detection Papers

### IDS-1: Closed-World Assumption
- Does evaluation assume all attack types are known?
- Is zero-day detection capability assessed?
- What happens with attack types not in training data?

### IDS-2: Feature Preprocessing Inconsistency
- Is the same preprocessing applied to all methods being compared?
- Are preprocessing choices justified?
- Do different preprocessing choices significantly affect results?

### IDS-3: Dataset Age and Relevance
- Are datasets from the current decade?
- Do traffic patterns match modern networks (encrypted, cloud-based)?
- Are IoT/IIoT-specific patterns relevant to the deployment scenario?

---

## §APT: Extra Pitfalls for APT Detection Papers

### APT-1: Temporal Scale Mismatch
- APTs operate over days/weeks/months; does the dataset capture this?
- Is the detection window (how far back the model looks) realistic?
- Can the system maintain state over the full APT lifecycle?

### APT-2: Single-Host vs. Multi-Host
- Is cross-host correlation evaluated?
- If the method claims to detect lateral movement, is it tested with multi-host scenarios?
- How many hosts are in the test environment?

### APT-3: Graph Explosion
- Provenance graphs grow unboundedly; is pruning/summarization discussed?
- What is the storage/memory cost of maintaining the graph?
- Is there a graph retention policy (time window, relevance-based)?

### APT-4: Attribution vs. Detection Conflation
- Does the paper conflate detection (is there an attack?) with attribution (who is the attacker?)?
- Are these tasks evaluated separately?

---

## Audit Summary Template

After completing the audit, fill in:

```markdown
# ML-Security Pitfalls Audit Summary

| # | Pitfall | Status | Evidence | Risk Level |
|---|---------|--------|----------|------------|
| P1 | Sampling Bias | | | |
| P2 | Label Inaccuracy | | | |
| P3 | Data Snooping | | | |
| P4 | Spurious Correlations | | | |
| P5 | Biased Parameters | | | |
| P6 | Inappropriate Baselines | | | |
| P7 | Inappropriate Measures | | | |
| P8 | Base Rate Fallacy | | | |
| P9 | Lab-Only Evaluation | | | |
| P10 | Inappropriate Threat Model | | | |

Pitfalls present (unaddressed): X/10
Pitfalls partially present: X/10
Pitfalls clean: X/10

Overall methodology risk: [Low / Medium / High]
Priority fixes: [list top 3 pitfalls to address]
```
