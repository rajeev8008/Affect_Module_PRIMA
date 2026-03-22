# PRIMA Affective Component — Project Summary

> **Purpose**: This document summarizes all 9 benchmarking studies, their classifications, and final baseline results (v2) with 95% Confidence Intervals for use in the research paper.
> **Framework**: Emotion AWARE (Gamage et al., Journal of Big Data, 2024)
> **Baseline Model**: DistilBERT-base (66M params) + GoEmotions + Plutchik 14-emotion lexicon (1,120 terms)

## 📊 Summary Comparison: Baseline vs. Paper

| Study | Category | Pillar | Metric | Baseline (v2) ± 95% CI | Paper Reference |
|---|---|---|---|---|---|
| **1** | 2-emo (ISEAR) | Elicitation | F1-weighted | **0.775 ± 0.021** (Acc: 0.79) | 0.898 |
| **2** | 4-common (ISEAR) | Elicitation | F1-weighted | **0.582 ± 0.031** | 0.812 |
| **3** | 4-rare (GoEmo) | Elicitation | F1-weighted | **0.466 ± 0.024** | 0.760 |
| **5** | Finance (PB) | Adaptability | F1-weighted | **0.784 ± 0.026** | 0.880 |
| **6** | Tech (Senti4SD) | Adaptability | F1-weighted | **0.712 ± 0.021** | 0.820 |
| **7** | Modifiers | Robustness | Intensity Δ | Orig: 0.62 | Int: 0.67 | Inh: 0.55 | Correct trend |
| **8** | Negation | Robustness | F1 (Negated) | **0.245** | 0.841 |

---

## 🔬 Detailed Study Breakdown

### I. Elicitation (Pillar 1)

#### Study 1: Two-emotion assembles (positive/negative) using ISEAR
- **Classification**: Elicitation
- **Goal**: Benchmark binary sentiment granularity.
- **Results**:
  | Class | Precision | Recall | F1 |
  |---|---|---|---|
  | Positive | 0.765 ± 0.027 | 0.785 ± 0.026 | 0.775 ± 0.021 |
  | Negative | 0.812 ± 0.024 | 0.794 ± 0.024 | 0.803 ± 0.018 |

#### Study 2: Four common emotion assembles (anger, fear, sadness, joy) using ISEAR
- **Classification**: Elicitation
- **Goal**: Measure performance on high-frequency emotions.
- **Results (F1 Score)**:
  - Joy: 0.612 ± 0.034
  - Anger: 0.565 ± 0.041
  - Fear: 0.542 ± 0.045
  - Sadness: 0.598 ± 0.038
  - **Weighted Avg**: 0.582 ± 0.031

#### Study 3: Four rare emotion assembles (disgust, surprise, trust, anticipation) using GoEmotions
- **Classification**: Elicitation
- **Goal**: Evaluate performance on nuanced/rare emotions.
- **Results (F1 Score)**:
  - Disgust: 0.470 ± 0.044
  - Surprise: 0.340 ± 0.053
  - Trust: 0.549 ± 0.029
  - Anticipation: 0.392 ± 0.039

#### Study 4: Elicitation of 2, 8, and 14 emotion assembles (Granularity)
- **Classification**: Elicitation
- **Goal**: Demonstrate cross-granularity consistency.
- **Demos**:
  - *"That's a maryland fan comment. You should be ashamed of yourself."* -> 14-emo: **disgust** (0.55); 8-emo: **disgust**; 2-emo: **negative**.
  - *"Our father will protect us <3"* -> 14-emo: **trust** (0.52); 8-emo: **trust**; 2-emo: **positive**.

---

### II. Adaptability (Pillar 2)

#### Study 5: Finance sector results (Financial PhraseBank)
- **Classification**: Adaptability (Domain)
- **Results**:
  - Positive F1: 0.824 ± 0.024
  - Negative F1: 0.643 ± 0.046

#### Study 6: Technology sector results (Senti4SD)
- **Classification**: Adaptability (Domain)
- **Results**:
  - Positive F1: 0.745 ± 0.021
  - Negative F1: 0.685 ± 0.021

---

### III. Robustness (Pillar 3)

#### Study 7: Robustness to Intensifiers and Inhibitors (Modifiers)
- **Classification**: Robustness
- **Goal**: Validate that intensity modifiers correctly shift emotion scores.
- **Intensity Means**:
  - Original: **0.6219**
  - Intensified (Extremely...): **0.6720** (↑)
  - Inhibited (Partly...): **0.5474** (↓)

#### Study 8: Robustness in Negation Detection
- **Classification**: Robustness
- **Goal**: Validate emotion flipping (e.g., "not happy" -> sadness).
- **Critical Finding**: Current baseline scores **0.2454** on negated sentences vs **0.8716** on original. The paper reports **0.841** on negated sentences, indicating a 60% performance gap in the baseline's negation handling.

---

### IV. Explainability (Pillar 4)

#### Study 9: Explainability with Window-based Keyword Retrieval
- **Classification**: Explainability
- **Goal**: Provide transparent evidence (keywords) for emotion scores.
- **Demo**:
  - *"Tiny felt very sad. The little prince was at first quite frightened at the bird... delighted, and thought her the prettiest..."*
  - **Top Keywords identified**: "frightened", "delighted", "sad".
  - **Top Predicted Emotion**: **joy_ecstasy** (0.34 - driven by 'delighted/prettiest'), followed by **fear** and **sadness**.
