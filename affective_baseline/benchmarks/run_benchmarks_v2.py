"""
Run all 9 Emotion AWARE benchmarking studies with enhanced metrics (v2).
Includes specific sentences from the AWARE paper (Gamage et al., 2024).
Usage: python -m benchmarks.run_benchmarks_v2
"""
import sys
import os
import json
import logging
import time
import pandas as pd
import ast
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmarks.run_benchmarks import BaselineDetector
from benchmarks.dataset_loader import (
    load_goemotions, load_isear, load_semeval2018,
    load_financial_phrasebank, load_senti4sd,
    get_modifier_dataset, get_negation_dataset
)
from benchmarks.evaluate_v2 import (
    evaluate_study1_binary, evaluate_study2_3_multiclass,
    evaluate_study5_6_domain, evaluate_study7_modifiers,
    evaluate_study8_negation, format_paper_tables
)
from Core.profile_builder import build_profile

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

# ============================================================
# PAPER-SPECIFIC SENTENCES (Tables 7, 10, 11, 14, 15)
# ============================================================

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

STUDY7_TABLE10_MODIFIERS = [
    ("Work was good for the first half", "–", 0),
    ("Work was incredibly good for the first half", "+", 0.9),
    ("Work was very good for the first half", "+", 0.8),
    ("Work was quite good for the first half", "+", 0.6),
    ("Work was considerably good for the first half", "+", 0.6),
    ("Work was almost good for the first half", "−", 0.2),
    ("Work was kinda good for the first half", "−", 0.3),
    ("Work was sort of good for the first half", "−", 0.4),
]

STUDY7_TABLE11 = [
    {"original": "She is happy", "intensified": "She is extremely happy", "inhibited": "She is partly happy", "emotion": "joy"}
]

STUDY9_TABLE14_SENTENCES = [
    'The son said: "Most gracious father, I will show her to you in the form of a beautiful flower," '
    'and he thrust his hand into his pocket and brought forth the pink, and placed it on the royal table, '
    'and it was so beautiful that the king had never seen one to equal it',
    'The king ordered the man to be brought before him, and threatened with angry words that unless he '
    'could before the morrow point out the thief, he himself should be looked upon as guilty and executed',
    '"It was saying, \'You are so beautiful, I like you very much. \'Tweet, tweet," sang the bird, '
    'as he flew out into the green woods, and Tiny felt very sad. The little prince was at first quite '
    'frightened at the bird. It was like a giant, compared to such a delicate little creature as himself. '
    'But when he saw Tiny, he was delighted, and thought her the prettiest little maiden he had ever seen',
]

# ============================================================
# RUN BENCHMARKS
# ============================================================

def run_v2_benchmarks(max_samples: int = None):
    detector = BaselineDetector()
    all_results = {}

    def limit(data):
        if max_samples and len(data) > max_samples:
            return data[:max_samples]
        return data

    # Study 1: Binary (ISEAR)
    logger.info("Running Study 1 (Binary ISEAR)...")
    isear = limit(load_isear())
    if isear:
        all_results["Study 1 (2-emo, ISEAR)"] = evaluate_study1_binary(detector.detect_2, isear)

    # Study 2: 4 Common Emotions (ISEAR)
    logger.info("Running Study 2 (4 Common ISEAR)...")
    if isear:
        study2_data = [s for s in isear if s["labels_8"][0] in ["joy", "anger", "fear", "sadness"]]
        study2_data = limit(study2_data)
        all_results["Study 2 (4-common, ISEAR)"] = evaluate_study2_3_multiclass(detector.detect_8, study2_data, ["joy", "anger", "fear", "sadness"])

    # Study 3: 4 Rare Emotions (GoEmotions)
    logger.info("Running Study 3 (4 Rare GoEmotions)...")
    goemo = limit(load_goemotions())
    if goemo:
        rare = ["disgust", "surprise", "trust", "anticipation"]
        study3_data = [s for s in goemo if s["labels_8"][0] in rare]
        study3_data = limit(study3_data)
        all_results["Study 3 (4-rare, GoEmotions)"] = evaluate_study2_3_multiclass(detector.detect_8, study3_data, rare)

    # Study 4: Granularity (Paper Sentences)
    logger.info("Running Study 4 (Granularity Demo)...")
    study4_res = []
    for s in STUDY4_PAPER_SENTENCES:
        s14 = detector.detect_14(s["text"])
        s8 = detector.detect_8(s["text"])
        s2 = detector.detect_2(s["text"])
        study4_res.append({
            "text": s["text"],
            "14_top": max(s14, key=s14.get) if s14 else "N/A",
            "8_top": max(s8, key=s8.get) if s8 else "N/A",
            "2_top": max(s2, key=s2.get) if s2 else "N/A",
        })
    all_results["Study 4 (Granularity)"] = {"demos": study4_res}

    # Study 5: Finance
    logger.info("Running Study 5 (Finance)...")
    fin = limit(load_financial_phrasebank())
    if fin:
        all_results["Study 5 (Finance, PhraseBank)"] = evaluate_study5_6_domain(detector.detect_2, fin)

    # Study 6: Tech
    logger.info("Running Study 6 (Tech)...")
    tech = limit(load_senti4sd())
    if tech:
        all_results["Study 6 (Tech, Senti4SD)"] = evaluate_study5_6_domain(detector.detect_2, tech)

    # Study 7: Modifiers
    logger.info("Running Study 7 (Modifiers)...")
    mod_data = get_modifier_dataset()
    all_results["Study 7 (Modifiers)"] = evaluate_study7_modifiers(detector.detect_8, mod_data)
    
    # Table 10/11 data
    t10_res = []
    for sent, val, intensity in STUDY7_TABLE10_MODIFIERS:
        scores = detector.detect_14(sent)
        top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:2]
        t10_res.append({"sent": sent, "val": val, "intensity": intensity, "top": top})
    all_results["Study 7 (Table 10)"] = t10_res

    # Study 8: Negation
    logger.info("Running Study 8 (Negation)...")
    neg_data = get_negation_dataset()
    all_results["Study 8 (Negation)"] = evaluate_study8_negation(detector.detect_8, neg_data)

    # Study 9: Explainability
    logger.info("Running Study 9 (Explainability)...")
    study9_res = []
    for sent in STUDY9_TABLE14_SENTENCES:
        pred = build_profile(sent, 1, detector.df, detector.tokenizer, detector.model, 
                             keyword_extraction=True, modifier_detection=True)
        study9_res.append({"text": sent, "keywords": pred[1], "scores": sorted(pred[0].items(), key=lambda x: x[1], reverse=True)[:5]})
    all_results["Study 9 (Explainability)"] = study9_res

    # Save results
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    with open(os.path.join(results_dir, "baseline_results_v2.json"), "w") as f:
        json.dump(all_results, f, indent=2, default=str)
        
    md_tables = format_paper_tables(all_results)
    with open(os.path.join(results_dir, "baseline_results_v2.md"), "w") as f:
        f.write(md_tables)
        
    logger.info(f"Results saved to {results_dir}")
    print("\n" + md_tables)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-samples", type=int, default=None)
    args = parser.parse_args()
    run_v2_benchmarks(max_samples=args.max_samples)
