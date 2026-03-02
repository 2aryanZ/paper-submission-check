---
name: paper-multi-round-review
description: Multi-round academic paper peer review simulation using multi-model diversity for improving paper quality before submission. Assigns different LLM models (Claude, GPT/Codex, Gemini) to 4 specialized reviewer roles (security domain expert, ML/GNN methods expert, experimental methodology expert, writing/presentation expert) plus a meta-reviewer and devil's advocate. Covers technical soundness, novelty, ML-for-security pitfalls, experimental rigor, and presentation quality. Supports multi-round cross-model review-rebuttal-revision cycles. Use when the user wants paper review, peer review simulation, technical feedback, paper improvement, strength/weakness analysis, or mentions reviewing, referee, rebuttal, or revision.
---

# Multi-Round Academic Paper Peer Review

Simulate a rigorous peer review process with multiple specialized reviewers to identify weaknesses and improve paper quality before submission. Modeled after top venues: NeurIPS, ICLR, USENIX Security, CCS, NDSS, IEEE S&P.

**Multi-model design**: This skill is designed for cross-model review diversity. Using a single model for all reviewer roles creates echo chamber effects — see [multi-model-strategy.md](multi-model-strategy.md) for the rationale and model assignment guide.

## Workflow Overview

```
Multi-Round Review Progress:
- [ ] Phase 0: Paper Intake (read paper, identify venue/domain, select reviewer panel)
- [ ] Phase 1: Independent Reviews (4 reviewers in parallel)
- [ ] Phase 2: Meta-Review Synthesis (AC aggregates, identifies consensus/divergence)
- [ ] Phase 3: Author Response Guidance (draft rebuttal strategy)
- [ ] Phase 4: Revision Execution (implement changes with diff tracking)
- [ ] Phase 5: Re-Review (reviewers reassess, update scores)
- [ ] Phase 6: Final Polish (handoff to paper-submission-check skill if available)
```

---

## Phase 0: Paper Intake & Model Assignment

Before reviewing, gather context and plan model allocation:

1. **Read the full paper** (all .tex files and .bib)
2. **Identify target venue type**:
   - Security conference (USENIX, CCS, NDSS, S&P) → emphasize threat model, real-world applicability
   - ML conference (NeurIPS, ICLR, ICML) → emphasize novelty, theoretical grounding, ablations
   - Journal (IEEE TDSC/TIFS, ACM TOPS) → emphasize completeness, reproducibility
   - Cross-domain (ML + Security) → apply BOTH sets of criteria
3. **Detect paper domain**: APT/intrusion detection, malware, vulnerability, privacy, etc.
4. **Count pages** and check against venue limit
5. **Assign models to roles** — see [multi-model-strategy.md](multi-model-strategy.md) for recommended assignments. If only one model is available, see the single-model mitigation protocol in that file

---

## Phase 1: Independent Reviews

Run 4 reviewer personas **independently** (parallel is preferred when sub-agents are available; sequential is acceptable as a fallback). Each reviewer MUST read the paper in full before reviewing. Each review MUST cite specific line numbers or section references.

### Reviewer Panel & Model Assignment

| Role | Expertise | Recommended Model | Focus | Reference |
|------|-----------|-------------------|-------|-----------|
| **Reviewer A** | Domain Expert | Gemini (web search + 1M context) | Threat model, attack realism, dataset quality, domain baselines | [reviewer-profiles.md](reviewer-profiles.md) §A |
| **Reviewer B** | Methods Expert | GPT/Codex (strongest math reasoning) | Model correctness, novelty, complexity, ablation completeness | [reviewer-profiles.md](reviewer-profiles.md) §B |
| **Reviewer C** | Methodology Expert | Claude (systematic checklist execution) | ML pitfalls, statistical rigor, reproducibility, fair comparison | [reviewer-profiles.md](reviewer-profiles.md) §C |
| **Reviewer D** | Presentation Expert | Claude (best writing quality sense) | Structure, clarity, figures, notation, related work coverage | [reviewer-profiles.md](reviewer-profiles.md) §D |
| **Devil's Advocate** | Adversarial Critic | Different from primary reviewers | Attack strongest claims, find fatal flaws | [multi-model-strategy.md](multi-model-strategy.md) §Devil |

For model assignment rationale, see [multi-model-strategy.md](multi-model-strategy.md).
For detailed checklists per reviewer, see [review-dimensions.md](review-dimensions.md).

### Review Output Format (per reviewer)

```markdown
# Review — Reviewer [A/B/C/D]
Expertise: [role description]

## 1. Summary (3-5 sentences)
[What the paper does, core contribution, main finding]

## 2. Strengths
- **S1** [§X / Line Y]: [specific strength with evidence]
- **S2** [§X / Line Y]: ...
- **S3** [§X / Line Y]: ...

## 3. Weaknesses
- **W1** [§X / Line Y] ⬛ Critical: [specific issue, why it matters, suggested fix]
- **W2** [§X / Line Y] 🟧 Major: [specific issue, why it matters, suggested fix]
- **W3** [§X / Line Y] 🟨 Minor: [specific issue, suggested fix]

## 4. Questions for Authors
- **Q1**: [specific technical question requiring author response]
- **Q2**: ...

## 5. Missing References
[Papers the authors should cite and compare against]

## 6. Scores
| Dimension     | Score | Scale |
|---------------|-------|-------|
| Soundness     | X/4   | 1=poor, 2=fair, 3=good, 4=excellent |
| Presentation  | X/4   | 1=poor, 2=fair, 3=good, 4=excellent |
| Contribution  | X/4   | 1=poor, 2=fair, 3=good, 4=excellent |
| Overall       | X/10  | 1=reject ... 6=weak accept ... 10=award |
| Confidence    | X/5   | 1=guess ... 5=certain |

## 7. Verdict
[Strong Accept / Accept / Weak Accept / Borderline Accept / Borderline Reject / Reject]
One-sentence justification.
```

Verdict should be consistent with Overall score (recommended mapping: 8-10 = Strong Accept, 7 = Accept, 6 = Weak Accept, 5 = Borderline Accept, 4 = Borderline Reject, 1-3 = Reject).

### Severity Definitions

| Level | Symbol | Meaning | Author Action |
|-------|--------|---------|---------------|
| Critical | ⬛ | Invalidates core claims; must fix or paper fails | Must address in revision |
| Major | 🟧 | Significantly weakens paper; strongly advised to fix | Should address; explain if cannot |
| Minor | 🟨 | Improvement opportunity; won't cause rejection alone | Nice to fix |

---

## Phase 2: Meta-Review Synthesis

After all 4 reviews, produce a meta-review as Area Chair:

```markdown
# Meta-Review (Area Chair Synthesis)

## Consensus Strengths
[Points all/most reviewers agree are strong]

## Consensus Weaknesses
[Problems identified by 2+ reviewers — highest priority]

## Divergent Points
[Where reviewers disagree — needs discussion]

## Critical Path to Acceptance
Ordered list of must-fix items (from Critical → Major):
1. [Highest priority issue — which reviewer(s) raised it]
2. ...
3. ...

## Score Summary
| Reviewer | Soundness | Presentation | Contribution | Overall | Confidence |
|----------|-----------|--------------|--------------|---------|------------|
| A        |           |              |              |         |            |
| B        |           |              |              |         |            |
| C        |           |              |              |         |            |
| D        |           |              |              |         |            |
| **Mean** |           |              |              |         |            |

## Preliminary Decision
[Strong Accept / Accept / Weak Accept / Borderline Accept / Borderline Reject / Revise & Resubmit / Reject]
```

---

## Phase 3: Author Response Guidance

For each weakness and question, draft a rebuttal strategy:

```markdown
# Rebuttal Plan

## W1 [Reviewer X]: [issue title]
- **Response type**: [New experiment / Clarification / Rewrite / Acknowledge limitation]
- **Action**: [Specific modification to make]
- **Evidence**: [What to add — new table, figure, paragraph, citation]
- **Effort**: [Low / Medium / High]

## Q1 [Reviewer X]: [question]
- **Answer**: [Draft answer]
- **Revision needed**: [Yes — describe change / No — clarification only]
```

Prioritization rule: Address ALL Critical items first, then Major items that 2+ reviewers raised, then remaining Major items, then Minor items if space permits.

---

## Phase 4: Revision Execution

For each planned revision:

1. **Before editing**: Re-read the relevant section in full
2. **Make the change**: Edit the .tex file with precise modifications
3. **Track changes**: Note what was modified (section, line range, nature of change)
4. **Verify consistency**: Check that the change doesn't contradict other sections (especially Abstract ↔ Results, Introduction claims ↔ Experiments)
5. **Cross-check numbers**: Any new numbers in text must match their source tables

### Revision Log Format

```markdown
# Revision Log

| # | Addresses | Section | Change Description | Lines |
|---|-----------|---------|-------------------|-------|
| 1 | W1 (Rev A) | §5.2 | Added statistical significance test results | 450-465 |
| 2 | Q2 (Rev B) | §4.1 | Clarified edge weight computation formula | 280-295 |
| ...| | | | |
```

---

## Phase 5: Re-Review (Cross-Model Verification)

After revisions, re-review with **cross-model verification** — the model that re-reviews should differ from the model that wrote the original review when possible. This prevents the "self-satisfied rebuttal" problem where a model accepts its own fixes too easily.

For each reviewer role:

1. **Check each addressed weakness**: Was it adequately resolved?
2. **Check for new issues**: Did the revision introduce problems?
3. **Update scores**: Adjust scores up or down with justification
4. **Final verdict**: Accept / Still needs revision / Reject

Re-review output is a shorter version of the Phase 1 format, focusing on delta assessment.

### Cross-Model Re-Review Matrix

| Original Reviewer | Re-Review Model | Rationale |
|-------------------|-----------------|-----------|
| Gemini (Rev A) | Claude or GPT | Different model verifies domain claims |
| GPT (Rev B) | Claude | Different model checks if math fixes are correct |
| Claude (Rev C) | GPT | Different model verifies methodology fixes |
| Claude (Rev D) | Gemini | Different model reassesses writing quality |

---

## Phase 6: Final Polish

After all reviews pass, hand off to the `paper-submission-check` skill (if available) for formatting, AI-style removal, citation, and LaTeX quality checks. This skill focuses on **technical depth**; `paper-submission-check` focuses on **surface quality**. Both are needed before submission.

---

## Domain-Specific Review Modules

When the paper falls into a specific domain, load additional review criteria:

| Domain | Extra Criteria | Reference |
|--------|---------------|-----------|
| ML + Security | 10 ML-security pitfalls audit | [ml-security-pitfalls.md](ml-security-pitfalls.md) |
| Network intrusion detection | Dataset quality, base rate, real-world gap | [ml-security-pitfalls.md](ml-security-pitfalls.md) §IDS |
| Provenance graph / APT | Threat model, DARPA datasets, scalability | [ml-security-pitfalls.md](ml-security-pitfalls.md) §APT |
| GNN / Graph learning | Expressiveness, over-smoothing, scalability | [review-dimensions.md](review-dimensions.md) §GNN |

---

## Scoring Rubric Reference

### Overall Rating (1-10, NeurIPS scale)

| Score | Label | Criteria |
|-------|-------|----------|
| 10 | Award quality | Technically flawless, groundbreaking impact, exceptional evaluation |
| 8-9 | Strong Accept | Novel ideas, strong impact, excellent evaluation and reproducibility |
| 7 | Accept | Technically solid, high impact on at least one sub-area, good evaluation |
| 6 | Weak Accept | Technically solid, moderate impact, no major concerns |
| 5 | Borderline Accept | Solid but reasons to accept only slightly outweigh reasons to reject |
| 4 | Borderline Reject | Solid but reasons to reject outweigh reasons to accept |
| 3 | Reject | Technical flaws, weak evaluation, inadequate reproducibility |
| 1-2 | Strong Reject | Major flaws, trivial results, or unaddressed ethical issues |

### Sub-Scores (1-4)

| Score | Soundness | Presentation | Contribution |
|-------|-----------|--------------|--------------|
| 4 | Claims fully supported, rigorous methodology | Crystal clear, excellent contextualization | Important questions, significant originality, valuable results |
| 3 | Claims mostly supported, minor gaps | Clear with minor issues | Reasonable questions, good originality |
| 2 | Notable gaps in evidence or methodology | Unclear in places, weak contextualization | Incremental or limited novelty |
| 1 | Core claims unsupported, serious flaws | Hard to follow, poor organization | Trivial contribution |

---

## Additional Resources

- Multi-model strategy and single-model fallback: [multi-model-strategy.md](multi-model-strategy.md)
- Detailed reviewer role definitions and persona prompts: [reviewer-profiles.md](reviewer-profiles.md)
- Complete review dimension checklists per reviewer: [review-dimensions.md](review-dimensions.md)
- ML-for-security 10 pitfalls audit guide: [ml-security-pitfalls.md](ml-security-pitfalls.md)
- Example review reports (accept and reject cases): [review-examples.md](review-examples.md)
