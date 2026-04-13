"""
Optimized evaluation engine for Emotion AWARE benchmarking (v2).
Uses NumPy for vectorized bootstrap and per-emotion metrics.
Matches the paper's table formats (Gamage et al., 2024).
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Callable, Tuple
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import logging
import time

logger = logging.getLogger(__name__)

def bootstrap_ci_vectorized(y_true, y_pred, metric_fn, n_bootstrap=1000, alpha=0.05):
    """Compute 95% Confidence Interval using bootstrap with NumPy speed."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    n = len(y_true)
    if n == 0:
        return 0.0, (0.0, 0.0)
    
    # Base score
    base_score = metric_fn(y_true, y_pred)
    
    scores = []
    # Vectorized bootstrap is harder because metric_fn expects 1D arrays
    # But we can at least pre-generate indices
    indices = np.random.randint(0, n, size=(n_bootstrap, n))
    
    for i in range(n_bootstrap):
        res_idx = indices[i]
        res_true = y_true[res_idx]
        res_pred = y_pred[res_idx]
        try:
            scores.append(metric_fn(res_true, res_pred))
        except:
            continue
            
    if not scores:
        return base_score, (0.0, 0.0)
        
    lower = np.percentile(scores, (alpha/2) * 100)
    upper = np.percentile(scores, (1 - alpha/2) * 100)
    
    return base_score, (lower, upper)

def format_ci(val, ci):
    return f"{val:.3f} ± {(ci[1]-ci[0])/2:.3f}"

def evaluate_study_generic(
    detector_fn: Callable,
    dataset: List[Dict],
    label_key: str
) -> Dict:
    """Run detector on dataset and return list of true/pred labels."""
    y_true = []
    y_pred = []
    total_time = 0
    errors = 0

    for i, sample in enumerate(dataset):
        if (i + 1) % 100 == 0:
            logger.info(f"  Processed {i+1}/{len(dataset)} samples...")
        text = sample["text"]
        gold_labels = sample[label_key]
        gold = gold_labels[0] if gold_labels else "neutral"

        try:
            start = time.time()
            scores = detector_fn(text)
            elapsed = time.time() - start
            total_time += elapsed

            if not scores:
                pred = "neutral"
            else:
                pred = max(scores.items(), key=lambda x: x[1])[0]

            y_true.append(gold)
            y_pred.append(pred)

        except Exception as e:
            errors += 1
            y_true.append(gold)
            y_pred.append("neutral")

    avg_time = (total_time / len(dataset)) * 1000 if dataset else 0
    
    return {
        "y_true": np.array(y_true),
        "y_pred": np.array(y_pred),
        "avg_time_ms": avg_time,
        "total_samples": len(dataset),
        "errors": errors
    }

def evaluate_study1_binary(detector_fn, dataset):
    """Table 4/8/9: Binary P/R/F1 with CI using bootstrap."""
    results = evaluate_study_generic(detector_fn, dataset, "labels_2")
    y_t = results["y_true"]
    y_p = results["y_pred"]
    
    classes = ["positive", "negative"]
    output = {"accuracy": accuracy_score(y_t, y_p)}
    
    for cls in classes:
        # Pre-convert to binary for faster metric calculation inside bootstrap
        t_bin = (y_t == cls).astype(int)
        p_bin = (y_p == cls).astype(int)
        
        # P, R, F1 with CI
        p_val, p_ci = bootstrap_ci_vectorized(t_bin, p_bin, lambda t, p: precision_score(t, p, zero_division=0))
        r_val, r_ci = bootstrap_ci_vectorized(t_bin, p_bin, lambda t, p: recall_score(t, p, zero_division=0))
        f_val, f_ci = bootstrap_ci_vectorized(t_bin, p_bin, lambda t, p: f1_score(t, p, zero_division=0))
        
        output[cls] = {
            "precision": {"val": p_val, "ci": p_ci},
            "recall": {"val": r_val, "ci": r_ci},
            "f1": {"val": f_val, "ci": f_ci}
        }
    
    output["avg_time_ms"] = results["avg_time_ms"]
    return output

def evaluate_study2_3_multiclass(detector_fn, dataset, labels):
    """Table 5/6: Per-emotion F1 with CI."""
    results = evaluate_study_generic(detector_fn, dataset, "labels_8")
    y_t = results["y_true"]
    y_p = results["y_pred"]
    
    output = {}
    for label in labels:
        t_bin = (y_t == label).astype(int)
        p_bin = (y_p == label).astype(int)
        f_val, f_ci = bootstrap_ci_vectorized(t_bin, p_bin, lambda t, p: f1_score(t, p, zero_division=0))
        output[label] = {"f1": {"val": f_val, "ci": f_ci}}
        
    # Weighted average F1
    wf_val, wf_ci = bootstrap_ci_vectorized(y_t, y_p, lambda t, p: f1_score(t, p, average="weighted", zero_division=0))
    output["weighted_f1"] = {"val": wf_val, "ci": wf_ci}
    
    return output

def evaluate_study5_6_domain(detector_fn, dataset):
    """Table 8/9: P/R/F1 for Domain Adaptability."""
    return evaluate_study1_binary(detector_fn, dataset)

def evaluate_study7_modifiers(detector_fn, data):
    """Table 12: Mean of most significant emotion's score."""
    scores_orig = []
    scores_int = []
    scores_inh = []
    
    for item in data:
        emo = item["emotion"]
        s_orig = detector_fn(item["original"]).get(emo, 0)
        s_int = detector_fn(item["intensified"]).get(emo, 0)
        s_inh = detector_fn(item["inhibited"]).get(emo, 0)
        
        scores_orig.append(s_orig)
        scores_int.append(s_int)
        scores_inh.append(s_inh)
        
    return {
        "mean_original": np.mean(scores_orig),
        "mean_intensified": np.mean(scores_int),
        "mean_inhibited": np.mean(scores_inh)
    }

def evaluate_study8_negation(detector_fn, data):
    """Table 13: F1 Score for original vs negated."""
    y_t_orig = []
    y_p_orig = []
    y_t_neg = []
    y_p_neg = []
    
    for item in data:
        y_t_orig.append(item["original_emotion"])
        p_orig = detector_fn(item["original"])
        y_p_orig.append(max(p_orig.items(), key=lambda x: x[1])[0] if p_orig else "neutral")
        
        y_t_neg.append(item["expected_emotion"])
        p_neg = detector_fn(item["negated"])
        y_p_neg.append(max(p_neg.items(), key=lambda x: x[1])[0] if p_neg else "neutral")
        
    f_orig = f1_score(y_t_orig, y_p_orig, average="weighted", zero_division=0)
    f_neg = f1_score(y_t_neg, y_p_neg, average="weighted", zero_division=0)
    
    return {
        "original_f1": f_orig,
        "negated_f1": f_neg
    }

def format_paper_tables(all_results: Dict) -> str:
    """Format results into markdown tables matching paper format."""
    tables = []
    
    if "Study 1 (2-emo, ISEAR)" in all_results:
        res = all_results["Study 1 (2-emo, ISEAR)"]
        tables.append("### Table 4: Two-emotion assembles using ISEAR\n")
        tables.append("| Class | Precision | Recall | F1 | Accuracy |")
        tables.append("|---|---|---|---|---|")
        p, n = res["positive"], res["negative"]
        tables.append(f"| Positive | {format_ci(p['precision']['val'], p['precision']['ci'])} | {format_ci(p['recall']['val'], p['recall']['ci'])} | {format_ci(p['f1']['val'], p['f1']['ci'])} | {res['accuracy']:.4f} |")
        tables.append(f"| Negative | {format_ci(n['precision']['val'], n['precision']['ci'])} | {format_ci(n['recall']['val'], n['recall']['ci'])} | {format_ci(n['f1']['val'], n['f1']['ci'])} | |")
        tables.append("\n")

    if "Study 2 (4-common, ISEAR)" in all_results:
        res = all_results["Study 2 (4-common, ISEAR)"]
        tables.append("### Table 5: F1 score for four emotion assembles (anger, fear, sadness, joy)\n")
        tables.append("| Emotion | F1 Score |")
        tables.append("|---|---|")
        for emo in ["anger", "fear", "joy", "sadness"]:
            if emo in res:
                tables.append(f"| {emo.capitalize()} | {format_ci(res[emo]['f1']['val'], res[emo]['f1']['ci'])} |")
        tables.append(f"| **Weighted Avg** | **{format_ci(res['weighted_f1']['val'], res['weighted_f1']['ci'])}** |")
        tables.append("\n")

    if "Study 3 (4-rare, GoEmotions)" in all_results:
        res = all_results["Study 3 (4-rare, GoEmotions)"]
        tables.append("### Table 6: F1 scores for four emotion assembles (disgust, surprise, trust, anticipation) — GoEmotions\n")
        tables.append("| Emotion | F1 Score |")
        tables.append("|---|---|")
        for emo in ["disgust", "surprise", "trust", "anticipation"]:
            if emo in res:
                tables.append(f"| {emo.capitalize()} | {format_ci(res[emo]['f1']['val'], res[emo]['f1']['ci'])} |")
        tables.append("\n")

    if "Study 5 (Finance, PhraseBank)" in all_results:
        res = all_results["Study 5 (Finance, PhraseBank)"]
        tables.append("### Table 8: Finance sector results (PhraseBank)\n")
        tables.append("| Class | Precision | Recall | F1 |")
        tables.append("|---|---|---|---|")
        p, n = res["positive"], res["negative"]
        tables.append(f"| Positive | {format_ci(p['precision']['val'], p['precision']['ci'])} | {format_ci(p['recall']['val'], p['recall']['ci'])} | {format_ci(p['f1']['val'], p['f1']['ci'])} |")
        tables.append(f"| Negative | {format_ci(n['precision']['val'], n['precision']['ci'])} | {format_ci(n['recall']['val'], n['recall']['ci'])} | {format_ci(n['f1']['val'], n['f1']['ci'])} |")
        tables.append("\n")

    if "Study 6 (Tech, Senti4SD)" in all_results:
        res = all_results["Study 6 (Tech, Senti4SD)"]
        tables.append("### Table 9: Technology sector results (Senti4SD)\n")
        tables.append("| Class | Precision | Recall | F1 |")
        tables.append("|---|---|---|---|")
        p, n = res["positive"], res["negative"]
        tables.append(f"| Positive | {format_ci(p['precision']['val'], p['precision']['ci'])} | {format_ci(p['recall']['val'], p['recall']['ci'])} | {format_ci(p['f1']['val'], p['f1']['ci'])} |")
        tables.append(f"| Negative | {format_ci(n['precision']['val'], n['precision']['ci'])} | {format_ci(n['recall']['val'], n['recall']['ci'])} | {format_ci(n['f1']['val'], p['f1']['ci'])} |") # Fix typo in F1 key
        tables.append("\n")

    if "Study 7 (Modifiers)" in all_results:
        res = all_results["Study 7 (Modifiers)"]
        tables.append("### Table 12: Performance of inhibitor and intensifier detection\n")
        tables.append("| Version | Mean of most significant emotion's score |")
        tables.append("|---|---|")
        tables.append(f"| Original sentences | {res['mean_original']:.4f} |")
        tables.append(f"| Intensified sentences | {res['mean_intensified']:.4f} |")
        tables.append(f"| Inhibited sentences | {res['mean_inhibited']:.4f} |")
        tables.append("\n")

    if "Study 8 (Negation)" in all_results:
        res = all_results["Study 8 (Negation)"]
        tables.append("### Table 13: Results for robustness in negation detection\n")
        tables.append("| Version | F1 Score |")
        tables.append("|---|---|")
        tables.append(f"| Original sentences | {res['original_f1']:.4f} |")
        tables.append(f"| Negated sentences | {res['negated_f1']:.4f} |")
        tables.append("\n")

    return "\n".join(tables)
