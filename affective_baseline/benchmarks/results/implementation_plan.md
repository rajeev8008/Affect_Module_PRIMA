# Emotion-Wise Benchmarking — Implementation Plan

## Goal

Re-run all 9 benchmarking studies with **per-emotion Precision, Recall, F1 and 95% confidence intervals**, matching the paper's table format. Use existing proxy datasets. Use the paper's **exact sentences** for qualitative studies.

---

## Key Differences from Current Benchmarking

| Aspect | Current | New (v2) |
|---|---|---|
| Metrics | Overall accuracy/F1 only | **Per-emotion P/R/F1 ± 95% CI** |
| Study 1 | ISEAR proxy, overall | Per-class (positive/negative) P/R/F1 ± CI (Table 4) |
| Study 2 | ISEAR, overall F1 | Per-emotion F1 ± CI for anger/fear/sadness/joy (Table 5) |
| Study 3 | GoEmotions + SemEval, overall | Per-emotion F1 ± CI for disgust/surprise/trust/anticipation (Table 6) |
| Study 4 | 10 random GoEmotions samples | **Paper's Table 7 sentences** + more GoEmotions samples with full profiles |
| Study 5 | Binary overall | Per-class P/R/F1 ± CI + weighted avg (Table 8) |
| Study 6 | Binary overall | Per-class P/R/F1 ± CI + weighted avg (Table 9) |
| Study 7 | Intensifier/inhibitor acc only | Paper's **Table 10 sentence** + **Table 11** demo + mean scores (Table 12) |
| Study 8 | Overall negation acc/F1 | F1 for original vs negated (Table 13) |
| Study 9 | 5 demo sentences | Paper's **Table 14 sentences** + **Table 15 keyword frequency** analysis |

---

## Paper-Specific Sentences to Include

### Study 4 — Table 7 Sentences (Granularity Demo)

```python
STUDY4_PAPER_SENTENCES = [
    {"text": "That's a maryland fan comment. You should be ashamed of yourself.",
     "ground_truth": "embarrassment", "gt_polarity": "negative"},
    {"text": "Our father will protect us <3",
     "ground_truth": "caring", "gt_polarity": "positive"},
    {"text": "But I'm sort of confused as to how the pic was taken, sorry if you said it but I'm a bit stupid and tired",
     "ground_truth": "confusion", "gt_polarity": "negative"},
    {"text": "Best bedtime christmas story ever.",
     "ground_truth": "admiration", "gt_polarity": "positive"},
]
```

### Study 7 — Table 10 Sentence (Modifier Intensity Demo)

```python
STUDY7_TABLE10_SENTENCE = "Work was good for the first half"
STUDY7_TABLE10_MODIFIERS = [
    # (sentence, modifier_valence, modifier_intensity)
    ("Work was good for the first half", "–", 0),              # original
    ("Work was incredibly good for the first half", "+", 0.9),
    ("Work was very good for the first half", "+", 0.8),
    ("Work was quite good for the first half", "+", 0.6),
    ("Work was considerably good for the first half", "+", 0.6),
    ("Work was almost good for the first half", "−", 0.2),
    ("Work was kinda good for the first half", "−", 0.3),
    ("Work was sort of good for the first half", "−", 0.4),
]

# Table 11 demo
STUDY7_TABLE11 = {
    "original": "She is happy",
    "intensified": "She is extremely happy",
    "inhibited": "She is partly happy",
}
```

### Study 9 — Table 14 Sentences (Explainability Demo)

```python
STUDY9_TABLE14_SENTENCES = [
    # Positive sample
    'The son said: "Most gracious father, I will show her to you in the form of a beautiful flower," '
    'and he thrust his hand into his pocket and brought forth the pink, and placed it on the royal table, '
    'and it was so beautiful that the king had never seen one to equal it',
    # Negative sample
    'The king ordered the man to be brought before him, and threatened with angry words that unless he '
    'could before the morrow point out the thief, he himself should be looked upon as guilty and executed',
    # Mixed sample
    '"It was saying, \'You are so beautiful, I like you very much. \'Tweet, tweet," sang the bird, '
    'as he flew out into the green woods, and Tiny felt very sad. The little prince was at first quite '
    'frightened at the bird. It was like a giant, compared to such a delicate little creature as himself. '
    'But when he saw Tiny, he was delighted, and thought her the prettiest little maiden he had ever seen',
]

# Table 15 — validate against known keywords per emotion
STUDY9_TABLE15_KEYWORDS = {
    "fear": ["frightened", "terrified", "afraid", "uneasy", "alarmed", "fear", "cried", "trembling", "anxious", "trembled"],
    "anger": ["angry", "stupid", "angrily", "cried", "growled", "annoyed", "nasty", "rage", "fury", "refused"],
    "joy": ["happy", "pleased", "joy", "glad", "merry", "delighted", "beautiful", "rejoiced", "happily", "good"],
    "surprise": ["exclaimed", "astonished", "surprised", "heavens", "startled", "shocked", "bewildered", "yelping", "sudden", "interrupting"],
    "sadness": ["wept", "sad", "grieved", "cry", "sorrowfully", "poor", "unhappy", "mournfully", "troubled", "tears"],
}
```

---

## Proposed Changes

### [NEW] [evaluate_v2.py](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/benchmarks/evaluate_v2.py)

- `compute_per_class_prf(y_true, y_pred, target_classes)` → per-class Precision, Recall, F1
- `bootstrap_ci(y_true, y_pred, metric_fn, n_bootstrap=1000)` → 95% CI via bootstrap
- `evaluate_binary_study(detector_fn, dataset)` → Table 4/8/9 format
- `evaluate_multiclass_study(detector_fn, dataset, target_emotions)` → Table 5/6 format
- `evaluate_modifiers_detailed(detector_fn, data, paper_sentences)` → Table 10/11/12 format
- `evaluate_negation_detailed(detector_fn, data)` → Table 13 format
- `evaluate_explainability(detector_fn, paper_sentences)` → Table 14/15 format
- `format_paper_tables(all_results)` → Paper-ready markdown

### [NEW] [run_benchmarks_v2.py](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/benchmarks/run_benchmarks_v2.py)

Runner using the new evaluation functions. Hardcodes paper sentences above. Saves to `results/baseline_results_v2.json` and `results/baseline_results_v2.md`.

### [NO CHANGES] Existing files

`dataset_loader.py`, `evaluate.py`, `run_benchmarks.py` remain untouched.

---

## Verification Plan

### Quick Test
```bash
python -m benchmarks.run_benchmarks_v2 --max-samples 50
```

### Full Run
```bash
python -m benchmarks.run_benchmarks_v2
```

### Manual
- Compare table formats against paper Tables 4–15
- Verify paper-specific sentences produce expected output
- Update `project_summary.md` with new results
