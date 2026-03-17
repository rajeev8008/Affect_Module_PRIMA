"""
Evaluation engine for Emotion AWARE benchmarking.
Computes Accuracy, Precision, Recall, F1-Score for all studies.
"""
import numpy as np
from typing import List, Dict, Callable, Tuple
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import logging
import time

logger = logging.getLogger(__name__)


def get_dominant_emotion(scores: dict) -> str:
    """Get the emotion with the highest score from a score dict."""
    if not scores:
        return "neutral"
    return max(scores.items(), key=lambda x: x[1])[0]


def evaluate_classification(
    detector_fn: Callable,
    dataset: List[Dict],
    label_key: str = "labels_8",
    top_k: int = 1,
) -> Dict:
    """
    Run detector on each sample and compute metrics.
    
    Args:
        detector_fn: Function that takes text → dict of {emotion: score}
        dataset: List of dicts with 'text' and label_key
        label_key: Which label column to evaluate against ('labels_2', 'labels_8', 'labels_14')
        top_k: How many top predicted emotions to consider as "predicted"
    
    Returns:
        Dict with accuracy, precision, recall, f1, per_class metrics, and timing
    """
    y_true = []
    y_pred = []
    total_time = 0
    errors = 0

    for i, sample in enumerate(dataset):
        text = sample["text"]
        gold_labels = sample[label_key]

        # Use primary (first) gold label for single-label evaluation
        gold = gold_labels[0] if gold_labels else "neutral"

        try:
            start = time.time()
            scores = detector_fn(text)
            elapsed = time.time() - start
            total_time += elapsed

            # Get top-k predictions
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            pred = sorted_scores[0][0] if sorted_scores else "neutral"

            y_true.append(gold)
            y_pred.append(pred)

        except Exception as e:
            errors += 1
            if errors <= 5:
                logger.warning(f"  Error on sample {i}: {e}")
            y_true.append(gold)
            y_pred.append("neutral")

        if (i + 1) % 200 == 0:
            logger.info(f"  Processed {i+1}/{len(dataset)}...")

    # Get unique labels
    all_labels = sorted(set(y_true + y_pred))

    # Compute metrics
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)

    # Per-class F1
    per_class_f1 = {}
    for label in all_labels:
        binary_true = [1 if t == label else 0 for t in y_true]
        binary_pred = [1 if p == label else 0 for p in y_pred]
        per_class_f1[label] = f1_score(binary_true, binary_pred, zero_division=0)

    avg_time = (total_time / len(dataset)) * 1000 if dataset else 0  # ms

    results = {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_weighted": round(f1, 4),
        "per_class_f1": {k: round(v, 4) for k, v in per_class_f1.items()},
        "avg_time_ms": round(avg_time, 2),
        "total_samples": len(dataset),
        "errors": errors,
    }
    return results


def evaluate_modifiers(
    detector_fn: Callable,
    modifier_data: List[Dict],
) -> Dict:
    """
    Study 7: Test that intensified > original > inhibited for the dominant emotion.
    """
    correct_intensified = 0
    correct_inhibited = 0
    total = len(modifier_data)

    for item in modifier_data:
        emotion = item["emotion"]
        try:
            scores_orig = detector_fn(item["original"])
            scores_int = detector_fn(item["intensified"])
            scores_inh = detector_fn(item["inhibited"])

            s_orig = scores_orig.get(emotion, 0)
            s_int = scores_int.get(emotion, 0)
            s_inh = scores_inh.get(emotion, 0)

            if s_int > s_orig:
                correct_intensified += 1
            if s_inh < s_orig:
                correct_inhibited += 1
        except Exception as e:
            logger.warning(f"  Modifier error: {e}")

    return {
        "intensifier_accuracy": round(correct_intensified / total, 4) if total else 0,
        "inhibitor_accuracy": round(correct_inhibited / total, 4) if total else 0,
        "total_samples": total,
    }


def evaluate_negation(
    detector_fn: Callable,
    negation_data: List[Dict],
) -> Dict:
    """
    Study 8: Test that negation flips the emotion to its Plutchik opposite.
    """
    y_true = []
    y_pred = []

    for item in negation_data:
        expected = item["expected_emotion"]
        try:
            scores = detector_fn(item["negated"])
            pred = get_dominant_emotion(scores)
            y_true.append(expected)
            y_pred.append(pred)
        except Exception as e:
            logger.warning(f"  Negation error: {e}")
            y_true.append(expected)
            y_pred.append("neutral")

    acc = accuracy_score(y_true, y_pred) if y_true else 0
    f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0) if y_true else 0

    return {
        "negation_accuracy": round(acc, 4),
        "negation_f1": round(f1, 4),
        "total_samples": len(negation_data),
    }


def format_results_table(all_results: Dict[str, Dict]) -> str:
    """Format all results into a markdown table for the dissertation."""
    # Map study names to their actual dataset sources
    dataset_map = {
        "Study 1 (2-emo, ISEAR)": "ISEAR (dair-ai/emotion)",
        "Study 2 (4-common, ISEAR)": "ISEAR (dair-ai/emotion)",
        "Study 3 (4-rare, GoEmotions)": "GoEmotions (go_emotions)",
        "Study 3 (4-rare, SemEval)": "SemEval (tweet_eval/emotion)",
        "Study 5 (Finance, PhraseBank)": "Twitter Financial News",
        "Study 6 (Tech, Senti4SD)": "SST-2 (Senti4SD proxy)",
    }

    lines = []
    lines.append("# Emotion AWARE Benchmarking Results")
    lines.append("")
    lines.append("| Study | Dataset | Metric | Score |")
    lines.append("|-------|---------|--------|-------|")

    for study_name, results in all_results.items():
        ds_name = dataset_map.get(study_name, study_name)
        if "f1_weighted" in results:
            lines.append(f"| {study_name} | {ds_name} | Accuracy | {results['accuracy']} |")
            lines.append(f"| | | Precision | {results['precision']} |")
            lines.append(f"| | | Recall | {results['recall']} |")
            lines.append(f"| | | F1 (weighted) | {results['f1_weighted']} |")
            lines.append(f"| | | Avg Time (ms) | {results['avg_time_ms']} |")
        elif "intensifier_accuracy" in results:
            lines.append(f"| {study_name} | Fairy Tales (80 synthetic) | Intensifier Acc | {results['intensifier_accuracy']} |")
            lines.append(f"| | | Inhibitor Acc | {results['inhibitor_accuracy']} |")
        elif "negation_f1" in results:
            lines.append(f"| {study_name} | Fairy Tales (80 synthetic) | Negation Acc | {results['negation_accuracy']} |")
            lines.append(f"| | | Negation F1 | {results['negation_f1']} |")

    return "\n".join(lines)
