"""
Run all 9 Emotion AWARE benchmarking studies on the baseline.
Usage: python -m benchmarks.run_benchmarks
"""
import sys
import os
import json
import logging
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import ast
import nltk
from transformers import AutoTokenizer, AutoModel
from Core.profile_builder import build_profile
from eight_and_fourteen import ft_to_et

from benchmarks.dataset_loader import (
    load_goemotions, load_isear, load_semeval2018,
    load_financial_phrasebank, load_senti4sd,
    get_modifier_dataset, get_negation_dataset,
    PLUTCHIK14_TO_8, PLUTCHIK8_TO_2,
)
from benchmarks.evaluate import (
    evaluate_classification, evaluate_modifiers,
    evaluate_negation, format_results_table,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

# Suppress noisy HuggingFace HTTP logs (the 404s are harmless fallback checks)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("datasets").setLevel(logging.WARNING)
logging.getLogger("huggingface_hub").setLevel(logging.WARNING)

# ============================================================
# BASELINE DETECTOR WRAPPER
# ============================================================

class BaselineDetector:
    """Wraps the baseline build_profile into a detector function."""

    def __init__(self):
        self.model_path = "joeddav/distilbert-base-uncased-go-emotions-student"
        self.vocab_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "Vocabularies", "goemotion_vocabulary.csv"
        )
        logger.info("Loading baseline model...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModel.from_pretrained(self.model_path)
        logger.info("Loading lexicon...")
        self.df = pd.read_csv(self.vocab_path)
        self.df = self.df.dropna()
        self.df['embedding'] = [ast.literal_eval(i) for i in self.df['embedding'].values.tolist()]
        logger.info(f"Baseline ready: {len(self.df)} lexicon terms.")

    def detect_14(self, text: str) -> dict:
        """Detect 14 Plutchik emotions from text."""
        try:
            pred = build_profile(
                text, 1, self.df, self.tokenizer, self.model,
                keyword_extraction=True, modifier_detection=True
            )
            return pred[0]  # scores dict
        except Exception as e:
            logger.warning(f"Detection error: {e}")
            return {}

    def detect_8(self, text: str) -> dict:
        """Detect 8 basic Plutchik emotions (collapses 14 → 8)."""
        scores_14 = self.detect_14(text)
        return ft_to_et(scores_14)

    def detect_2(self, text: str) -> dict:
        """Detect binary sentiment (collapses 14 → 8 → 2)."""
        scores_8 = self.detect_8(text)
        result = {"positive": 0, "negative": 0}
        for emo, score in scores_8.items():
            binary = PLUTCHIK8_TO_2.get(emo, "negative")
            result[binary] += score
        return result


# ============================================================
# RUN ALL 9 STUDIES
# ============================================================

def run_all_studies(max_samples: int = None):
    """
    Run all 9 AWARE benchmarking studies.
    Args:
        max_samples: Limit dataset size for faster testing (None = full dataset)
    """
    detector = BaselineDetector()
    all_results = {}

    def limit(data):
        if max_samples and len(data) > max_samples:
            return data[:max_samples]
        return data

    # ---- Study 1: Binary (2-emotion) on ISEAR ----
    logger.info("=" * 60)
    logger.info("STUDY 1: Binary Classification (Positive/Negative) — ISEAR")
    logger.info("=" * 60)
    isear = limit(load_isear())
    if isear:
        results = evaluate_classification(detector.detect_2, isear, label_key="labels_2")
        all_results["Study 1 (2-emo, ISEAR)"] = results
        logger.info(f"  F1: {results['f1_weighted']}  Acc: {results['accuracy']}")

    # ---- Study 2: 4 Common Emotions (joy, anger, fear, sadness) on ISEAR ----
    logger.info("=" * 60)
    logger.info("STUDY 2: 4 Common Emotions — ISEAR")
    logger.info("=" * 60)
    if isear:
        # Filter to only joy, anger, fear, sadness
        study2_data = [s for s in isear if s["labels_8"][0] in ["joy", "anger", "fear", "sadness"]]
        study2_data = limit(study2_data)
        if study2_data:
            results = evaluate_classification(detector.detect_8, study2_data, label_key="labels_8")
            all_results["Study 2 (4-common, ISEAR)"] = results
            logger.info(f"  F1: {results['f1_weighted']}  Acc: {results['accuracy']}")

    # ---- Study 3: 4 Rare Emotions (disgust, surprise, trust, anticipation) on GoEmotions ----
    logger.info("=" * 60)
    logger.info("STUDY 3: 4 Rare Emotions — GoEmotions + SemEval")
    logger.info("=" * 60)
    goemo = limit(load_goemotions())
    if goemo:
        # Filter to rare emotions
        rare = ["disgust", "surprise", "trust", "anticipation"]
        study3_data = [s for s in goemo if s["labels_8"][0] in rare]
        study3_data = limit(study3_data)
        if study3_data:
            results = evaluate_classification(detector.detect_8, study3_data, label_key="labels_8")
            all_results["Study 3 (4-rare, GoEmotions)"] = results
            logger.info(f"  F1: {results['f1_weighted']}  Acc: {results['accuracy']}")

    # SemEval component of Study 3
    semeval = limit(load_semeval2018())
    if semeval:
        study3b_data = [s for s in semeval if s["labels_8"][0] in rare]
        study3b_data = limit(study3b_data)
        if study3b_data:
            results = evaluate_classification(detector.detect_8, study3b_data, label_key="labels_8")
            all_results["Study 3 (4-rare, SemEval)"] = results
            logger.info(f"  F1: {results['f1_weighted']}  Acc: {results['accuracy']}")

    # ---- Study 4: Granularity Demo on GoEmotions ----
    logger.info("=" * 60)
    logger.info("STUDY 4: Multi-Granularity Demo — GoEmotions")
    logger.info("=" * 60)
    if goemo:
        demo_samples = goemo[:10]
        study4_results = []
        for sample in demo_samples:
            s14 = detector.detect_14(sample["text"])
            s8 = detector.detect_8(sample["text"])
            s2 = detector.detect_2(sample["text"])
            study4_results.append({
                "text": sample["text"][:80],
                "14_top": max(s14, key=s14.get) if s14 else "N/A",
                "8_top": max(s8, key=s8.get) if s8 else "N/A",
                "2_top": max(s2, key=s2.get) if s2 else "N/A",
            })
        all_results["Study 4 (Granularity)"] = {"demos": study4_results}
        for demo in study4_results:
            logger.info(f"  '{demo['text'][:50]}...' → 14:{demo['14_top']} | 8:{demo['8_top']} | 2:{demo['2_top']}")

    # ---- Study 5: Finance Domain — PhraseBank ----
    logger.info("=" * 60)
    logger.info("STUDY 5: Finance Domain — Financial PhraseBank")
    logger.info("=" * 60)
    fin = limit(load_financial_phrasebank())
    if fin:
        results = evaluate_classification(detector.detect_2, fin, label_key="labels_2")
        all_results["Study 5 (Finance, PhraseBank)"] = results
        logger.info(f"  F1: {results['f1_weighted']}  Acc: {results['accuracy']}")

    # ---- Study 6: Tech Domain — Senti4SD ----
    logger.info("=" * 60)
    logger.info("STUDY 6: Tech Domain — Senti4SD")
    logger.info("=" * 60)
    tech = limit(load_senti4sd())
    if tech:
        results = evaluate_classification(detector.detect_2, tech, label_key="labels_2")
        all_results["Study 6 (Tech, Senti4SD)"] = results
        logger.info(f"  F1: {results['f1_weighted']}  Acc: {results['accuracy']}")

    # ---- Study 7: Modifier Robustness ----
    logger.info("=" * 60)
    logger.info("STUDY 7: Modifier Robustness (Intensifiers/Inhibitors)")
    logger.info("=" * 60)
    mod_data = get_modifier_dataset()
    results = evaluate_modifiers(detector.detect_8, mod_data)
    all_results["Study 7 (Modifiers)"] = results
    logger.info(f"  Intensifier Acc: {results['intensifier_accuracy']}")
    logger.info(f"  Inhibitor Acc: {results['inhibitor_accuracy']}")

    # ---- Study 8: Negation Robustness ----
    logger.info("=" * 60)
    logger.info("STUDY 8: Negation Robustness")
    logger.info("=" * 60)
    neg_data = get_negation_dataset()
    results = evaluate_negation(detector.detect_8, neg_data)
    all_results["Study 8 (Negation)"] = results
    logger.info(f"  Negation Acc: {results['negation_accuracy']}")
    logger.info(f"  Negation F1: {results['negation_f1']}")

    # ---- Study 9: Explainability Demo ----
    logger.info("=" * 60)
    logger.info("STUDY 9: Explainability (Keyword Extraction)")
    logger.info("=" * 60)
    demo_sentences = [
        "I am terrified of public speaking.",
        "The sunset was absolutely beautiful and calming.",
        "I am furious about the unfair treatment.",
        "She was surprised by the unexpected gift.",
        "The news made me deeply sad.",
    ]
    study9_results = []
    for sent in demo_sentences:
        pred = build_profile(
            sent, 1, detector.df, detector.tokenizer, detector.model,
            keyword_extraction=True, modifier_detection=True
        )
        scores = pred[0]
        keywords = pred[1] if len(pred) > 1 else []
        top_emo = max(scores, key=scores.get) if scores else "N/A"
        top_score = max(scores.values()) if scores else 0
        study9_results.append({
            "text": sent,
            "detected": top_emo,
            "score": round(top_score, 3),
            "keywords": keywords,
        })
        logger.info(f"  '{sent}' → {top_emo} ({top_score:.3f}) | Keywords: {keywords}")

    all_results["Study 9 (Explainability)"] = {"demos": study9_results}

    # ---- SAVE RESULTS ----
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(results_dir, exist_ok=True)

    results_path = os.path.join(results_dir, "baseline_results.json")
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    logger.info(f"\nResults saved to: {results_path}")

    # Print summary table
    table = format_results_table(all_results)
    print("\n" + table)

    table_path = os.path.join(results_dir, "baseline_results.md")
    with open(table_path, "w") as f:
        f.write(table)
    logger.info(f"Table saved to: {table_path}")

    return all_results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run AWARE benchmarks on baseline")
    parser.add_argument("--max-samples", type=int, default=None,
                        help="Limit samples per dataset (for quick testing)")
    args = parser.parse_args()

    run_all_studies(max_samples=args.max_samples)
