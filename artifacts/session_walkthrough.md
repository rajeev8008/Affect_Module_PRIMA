# PRIMA Affective Module — Session Walkthrough & Findings

> **Date**: 26 March 2026
> **Scope**: Full analysis of the affective_baseline module — benchmarks, negation, subtle emotions, and improvement paths

---

## 1. Benchmark Results Overview

### Files Identified
- **1st Benchmark**: `benchmarks/results/baseline_results.md` + `.json` (v1 — basic metrics)
- **2nd Benchmark**: `benchmarks/results/baseline_results_v2.md` + `.json` (v2 — per-emotion F1 with 95% CI)
- **Summary**: `benchmarks/results/project_summary.md`

### Benchmark v2 Scores vs Paper

| Study | Category | Metric | Baseline ± CI | Paper | Gap |
|-------|----------|--------|---------------|-------|-----|
| 1 — Binary (ISEAR) | Elicitation | F1 | 0.775 ± 0.021 | 0.898 | 14% |
| 2 — 4-Common (ISEAR) | Elicitation | F1 | 0.582 ± 0.031 | 0.812 | 28% |
| 3 — 4-Rare (GoEmo) | Elicitation | F1 | 0.466 ± 0.024 | 0.760 | 39% |
| 5 — Finance (PB) | Adaptability | F1 | 0.784 ± 0.026 | 0.880 | 11% |
| 6 — Tech (Senti4SD) | Adaptability | F1 | 0.712 ± 0.021 | 0.820 | 13% |
| 7 — Modifiers | Robustness | Intensity | Correct trend | — | OK |
| **8 — Negation** | **Robustness** | **F1** | **0.245** | **0.841** | **60%** |

> **Confidence Intervals**: All CIs (±0.021 to ±0.031) are in the ideal range of ±0.01–0.03, indicating statistically stable results.

---

## 2. Codebase Audit — 20 Issues Found

Full details in [issues_and_improvement_plan.md](file:///C:/Users/galad/.gemini/antigravity/brain/902257ea-0345-47f9-9bab-3e7b94cbb16b/issues_and_improvement_plan.md).

| Severity | Count | Key Issues |
|----------|-------|------------|
| 🔴 Critical | 3 | Negation detection broken, hardcoded paths, full-dict emotion flipping |
| 🟠 Major | 5 | Proxy datasets, no caching, brute-force KNN O(n) |
| 🟡 Moderate | 8 | Copy-paste bug in Study 6 CI, dead code, global variables |
| 🔵 Low | 4 | Duplicate functions, inconsistent returns |

---

## 3. Deep Dive: How Negation Detection Works

### The Pipeline (traced step by step)

```
Input: "I have never been afraid of the dark"
  ↓
Step 1: Split into sliding windows (window_size=1)
  → ["I have never been afraid of the dark", "I", "have", "never", "been", "afraid", "of", "the", "dark"]
  ↓
Step 2: Get DistilBERT embeddings for ALL pieces (9 embeddings)
  ↓
Step 3: KNN — cosine similarity of FULL sentence embedding vs 1,120 vocabulary terms
  → Top 50 nearest neighbors → rank-weighted scoring → emotion scores
  ↓
Step 4: Keyword extraction — find which individual word is most similar to full sentence
  → Top keyword = "afraid"
  ↓
Step 5: 3-token lookback from keyword → check for negation/modifiers
  → "have never been" → "never" found in negation list!
  ↓
Step 6: map_opposite_emotions() → flips ALL 14 emotion scores to Plutchik opposites
```

### The Problem: Two Systems Fighting

| System | What it does | Example result |
|--------|-------------|----------------|
| **DistilBERT (implicit)** | Contextual embedding already understands "never afraid" → shifts toward trust/positive | trust ↑ |
| **Rule-based (explicit)** | Detects "never" → flips ALL emotions via `map_opposite_emotions()` | fear→trust, trust→fear |

**Result**: Sometimes they both help (Scenario B), sometimes they fight (Scenario A), sometimes both miss (Scenario C). Net effect across 80 sentences = F1 of 0.245.

### Interactive Test Results (8 sentences)

| Input | Top Emotion | Score | Correct? |
|-------|-------------|-------|----------|
| She is happy | joy_ecstasy | 0.872 | ✅ |
| She is not happy | sadness | 0.438 | ✅ |
| I am afraid of the dark | fear | 0.578 | ✅ |
| I have never been afraid of the dark | trust | 0.511 | ✅ |
| The movie was not boring, it was exciting | joy_ecstasy | 0.710 | ✅ (keyword-driven) |
| He doesn't trust anyone anymore | sadness | 0.374 | ❌ (expected: disgust) |
| The children were not surprised by the gift | anticipation | 0.271 | ✅ (accidental) |
| I am not angry with you I forgive you | acceptance | 0.325 | ⚠️ (keyword "forgive" drove it) |

---

## 4. Experiment: Disabling Rule-Based Negation Flip (Option A)

**What we did**: Commented out the `map_opposite_emotions()` call in `modifier_handling.py`.

**Result**: Mixed — some cases improved, others got worse.

| Sentence | Before (flip ON) | After (flip OFF) | Better? |
|----------|-------------------|-------------------|---------|
| She is not happy | sadness ✅ | sadness ✅ | Same |
| I have never been afraid | trust ✅ | fear ❌ | Worse |
| The princess was not happy | sadness ✅ | sadness ✅ | Same |
| He doesn't trust anyone | sadness ❌ | sadness ❌ | Same |
| Children not surprised | anticipation ✅ | joy_ecstasy ❌ | Worse |

> **Conclusion**: Disabling the rule-based flip **does not help**. Neither DistilBERT alone nor the rule-based system alone is sufficient. A coordinated approach (Option B) is needed.

**Change was reverted** — codebase is back to original.

---

## 5. External Model Evaluation

### `Sidharthan/roberta-base-conv-emotion` (RoBERTa fine-tuned on Empathetic Dialogues)

| Factor | Assessment |
|--------|------------|
| Emotions | 8 classes: Surprised, Angry, Sad, Joyful, Anxious, Hopeful, Confident, Disappointed |
| Plutchik match | Only 4/8 map directly; "Disappointed ≠ Disgust", "Confident ≠ Trust" |
| Architecture | Classifier (outputs labels) vs current embedder (cosine similarity) |
| Training data | Conversational dialogues — different domain from benchmarks |
| Verdict | **Not compatible** — would require full pipeline redesign |

**Better alternatives**: `SamLowe/roberta-base-go_emotions` (28 GoEmotions labels, Plutchik-compatible).

---

## 6. Subtle Emotion Test (No Explicit Emotion Words)

Full results in [subtle_emotion_test_results.md](file:///C:/Users/galad/.gemini/antigravity/brain/902257ea-0345-47f9-9bab-3e7b94cbb16b/subtle_emotion_test_results.md).

### Overall: 9/24 = 37.5% (3x random baseline)

| Emotion | Score | Key Finding |
|---------|-------|-------------|
| 🟢 Anticipation | 3/3 | Perfect — "preparing", "booked", "countdown" all matched |
| 🟡 Sadness | 2/3 | "goodbye", "empty" worked; "last train" missed |
| 🟡 Trust | 2/3 | "safe" worked; "things go wrong" confused it |
| 🟠 Joy | 1/3 | Only "greet" worked |
| 🟠 Anger | 1/3 | Only "scratched" worked |
| 🔴 Fear | 0/3 | All classified as anticipation (adjacent on Plutchik wheel) |
| 🔴 Disgust | 0/3 | "cockroach in soup" → surprise |
| 🔴 Surprise | 0/3 | All misclassified |

### Key Insights
1. **Keyword-dependent**: Works when emotion-bearing words exist, fails on purely situational context
2. **Fear ↔ Anticipation confusion**: Systematic — both represent "something coming", model can't distinguish threat vs. excitement
3. **Trust over-prediction**: Appeared as false positive 5 times across different emotions
4. **Cannot do commonsense reasoning**: "500 people" = scary requires world knowledge the model doesn't have

---

## 7. Conclusions & Path Forward

### What Works Well
- ✅ Explicit emotion detection (joy_ecstasy=0.872 for "She is happy")
- ✅ Binary sentiment (Study 1: F1=0.775)
- ✅ Finance domain adaptation (Study 5: F1=0.784)
- ✅ Modifier detection (intensifiers/inhibitors follow correct trend)
- ✅ Anticipation detection (perfect on subtle test)

### What Doesn't Work
- ❌ Negation handling (Study 8: F1=0.245 — two systems fighting)
- ❌ Subtle/situational emotions (37.5% without explicit words)
- ❌ Fear, disgust, surprise detection without keywords
- ❌ Sarcasm / commonsense reasoning

### Improvement Priority (unchanged)

| Priority | Action | Impact |
|----------|--------|--------|
| 1 | **Fix negation (Option B: nudge, don't flip)** | Study 8: 0.245 → ~0.6 |
| 2 | **Replace with GoEmotions RoBERTa** | All studies +5-10% |
| 3 | **Use actual datasets (not proxies)** | Accurate paper comparison |
| 4 | **Vectorize KNN** | 10-50x speed improvement |
| 5 | **Memory + Reflection integration** | Context-aware + commonsense | 

> [!IMPORTANT]
> The affect module alone cannot solve contextual/situational emotion understanding. The Memory and Reflection modules are essential for handling sarcasm, world knowledge ("500 people = scary"), and personal emotional patterns. Awaiting architectures from user.
