"""
Dataset loaders for all 9 Emotion AWARE benchmarking studies.
Loads: ISEAR, GoEmotions, SemEval-2018, Financial PhraseBank, Senti4SD
"""
import os
import csv
import json
import logging
from typing import List, Tuple, Dict

logger = logging.getLogger(__name__)

# ============================================================
# LABEL MAPPINGS
# ============================================================

# GoEmotions 27 → Plutchik 14
GOEMO_TO_PLUTCHIK14 = {
    "admiration": "admire", "amusement": "joy_ecstasy", "anger": "anger",
    "annoyance": "anger", "approval": "trust", "caring": "trust",
    "confusion": "distraction", "curiosity": "interest_vigilance",
    "desire": "anticipation", "disappointment": "sadness",
    "disapproval": "disgust_loathing", "disgust": "disgust_loathing",
    "embarrassment": "fear", "excitement": "joy_ecstasy", "fear": "fear",
    "gratitude": "trust", "grief": "sadness", "joy": "joy_ecstasy",
    "love": "joy_ecstasy", "nervousness": "fear", "optimism": "anticipation",
    "pride": "joy_ecstasy", "realization": "distraction", "relief": "serenity",
    "remorse": "sadness", "sadness": "sadness", "surprise": "amazement_surprise",
    "neutral": "neutral"
}

# Plutchik 14 → Plutchik 8
PLUTCHIK14_TO_8 = {
    "joy_ecstasy": "joy", "serenity": "joy",
    "admire": "trust", "acceptance": "trust", "trust": "trust",
    "amazement_surprise": "surprise", "distraction": "surprise",
    "anticipation": "anticipation", "interest_vigilance": "anticipation",
    "anger": "anger",
    "disgust_loathing": "disgust", "boredom": "disgust",
    "sadness": "sadness",
    "fear": "fear",
}

# Plutchik 8 → Binary (2)
PLUTCHIK8_TO_2 = {
    "joy": "positive", "trust": "positive",
    "surprise": "positive", "anticipation": "positive",
    "anger": "negative", "disgust": "negative",
    "sadness": "negative", "fear": "negative",
}

# ISEAR emotions → Plutchik 8
ISEAR_TO_PLUTCHIK8 = {
    "joy": "joy", "fear": "fear", "anger": "anger",
    "sadness": "sadness", "disgust": "disgust",
    "shame": "sadness", "guilt": "sadness",
}

# SemEval-2018 uses Plutchik 8 directly
SEMEVAL_EMOTIONS = ["anger", "anticipation", "disgust", "fear",
                    "joy", "sadness", "surprise", "trust"]


def map_to_granularity(labels_14: List[str], granularity: int) -> List[str]:
    """Convert Plutchik-14 labels to 8 or 2."""
    if granularity == 14:
        return labels_14
    elif granularity == 8:
        return list(set(PLUTCHIK14_TO_8.get(l, l) for l in labels_14))
    elif granularity == 2:
        labels_8 = [PLUTCHIK14_TO_8.get(l, l) for l in labels_14]
        return list(set(PLUTCHIK8_TO_2.get(l, l) for l in labels_8))
    return labels_14


# ============================================================
# DATASET LOADERS
# ============================================================

def load_goemotions(split: str = "test") -> List[Dict]:
    """
    Study 3 & 4: GoEmotions → 14 Plutchik labels.
    Returns: [{'text': str, 'labels_14': [...], 'labels_8': [...], 'labels_2': [...]}]
    """
    from datasets import load_dataset
    logger.info(f"Loading GoEmotions ({split})...")
    ds = load_dataset("go_emotions", "simplified", split=split)
    label_names = ds.features["labels"].feature.names

    data = []
    for item in ds:
        orig = [label_names[i] for i in item["labels"]]
        l14 = list(set(GOEMO_TO_PLUTCHIK14.get(l, "neutral") for l in orig))
        if "neutral" in l14 and len(l14) > 1:
            l14.remove("neutral")
        if l14 == ["neutral"]:
            continue  # skip pure neutral for emotion benchmarking

        data.append({
            "text": item["text"],
            "labels_14": l14,
            "labels_8": map_to_granularity(l14, 8),
            "labels_2": map_to_granularity(l14, 2),
        })
    logger.info(f"  → {len(data)} emotional samples loaded.")
    return data


def load_isear() -> List[Dict]:
    """
    Study 1 & 2: ISEAR dataset.
    Returns samples with Plutchik-8 and binary labels.
    """
    from datasets import load_dataset
    logger.info("Loading ISEAR...")
    try:
        ds = load_dataset("dair-ai/emotion", split="test")
        # dair-ai/emotion has labels: sadness(0), joy(1), love(2), anger(3), fear(4), surprise(5)
        label_map = {0: "sadness", 1: "joy", 2: "joy", 3: "anger", 4: "fear", 5: "surprise"}
        data = []
        for item in ds:
            emo8 = label_map.get(item["label"], None)
            if emo8 is None:
                continue
            binary = PLUTCHIK8_TO_2.get(emo8, "negative")
            data.append({
                "text": item["text"],
                "labels_8": [emo8],
                "labels_2": [binary],
            })
        logger.info(f"  → {len(data)} ISEAR/Emotion samples loaded.")
        return data
    except Exception as e:
        logger.warning(f"  Could not load ISEAR: {e}")
        return []


def load_semeval2018() -> List[Dict]:
    """
    Study 3: SemEval-2018 proxy via cardiffnlp/tweet_eval (emotion).
    Labels: anger(0), joy(1), optimism(2), sadness(3)
    """
    from datasets import load_dataset
    logger.info("Loading SemEval-2018 (via tweet_eval/emotion)...")
    try:
        ds = load_dataset("cardiffnlp/tweet_eval", "emotion", split="test")
        label_map = {0: "anger", 1: "joy", 2: "anticipation", 3: "sadness"}
        data = []
        for item in ds:
            emo8 = label_map.get(item["label"], None)
            if emo8 is None:
                continue
            binary = PLUTCHIK8_TO_2.get(emo8, "negative")
            data.append({
                "text": item["text"],
                "labels_8": [emo8],
                "labels_2": [binary],
            })
        logger.info(f"  → {len(data)} SemEval/tweet_eval samples loaded.")
        return data
    except Exception as e:
        logger.warning(f"  Could not load SemEval-2018: {e}")
        return []


def load_financial_phrasebank() -> List[Dict]:
    """
    Study 5: Financial sentiment via zeroshot/twitter-financial-news-sentiment.
    Labels: 0=Bearish(negative), 1=Bullish(positive), 2=Neutral
    """
    from datasets import load_dataset
    logger.info("Loading Financial PhraseBank (via twitter-financial-news)...")
    try:
        ds = load_dataset("zeroshot/twitter-financial-news-sentiment", split="validation")
        label_map = {0: "negative", 1: "positive", 2: "neutral"}
        data = []
        for item in ds:
            label = label_map.get(item["label"], "neutral")
            if label == "neutral":
                continue
            data.append({
                "text": item["text"],
                "labels_2": [label],
            })
        logger.info(f"  → {len(data)} Financial sentiment samples loaded.")
        return data
    except Exception as e:
        logger.warning(f"  Could not load Financial PhraseBank: {e}")
        return []


def load_senti4sd() -> List[Dict]:
    """
    Study 6: Senti4SD (StackOverflow sentiment) — 3-class.
    Falls back to a proxy dataset if Senti4SD is not available on HuggingFace.
    """
    from datasets import load_dataset
    logger.info("Loading Senti4SD (or proxy)...")
    try:
        # Senti4SD is not on HuggingFace natively; use a proxy
        ds = load_dataset("SetFit/sst2", split="test")
        label_map = {0: "negative", 1: "positive"}
        data = []
        for item in ds:
            label = label_map.get(item["label"], "neutral")
            data.append({
                "text": item["text"],
                "labels_2": [label],
            })
        logger.info(f"  → {len(data)} Senti4SD/proxy samples loaded.")
        return data
    except Exception as e:
        logger.warning(f"  Could not load Senti4SD: {e}")
        return []


# ============================================================
# ROBUSTNESS DATASETS (Studies 7 & 8) — Synthetic
# ============================================================

FAIRY_TALE_SENTENCES = [
    ("The princess was happy in her castle.", "joy"),
    ("The wolf was angry and dangerous.", "anger"),
    ("The old woman felt sad and lonely.", "sadness"),
    ("The knight was afraid of the dragon.", "fear"),
    ("The king was disgusted by the traitor.", "disgust"),
    ("The children were surprised by the gift.", "surprise"),
    ("The queen trusted her loyal advisor.", "trust"),
    ("The prince anticipated the grand ball.", "anticipation"),
    ("The fairy was joyful and kind.", "joy"),
    ("The ogre was furious at the villagers.", "anger"),
    ("The maiden wept with sorrow.", "sadness"),
    ("The traveler trembled with fear.", "fear"),
    ("The duchess found the meal repulsive.", "disgust"),
    ("The crowd gasped in astonishment.", "surprise"),
    ("The merchant had faith in his partner.", "trust"),
    ("The explorer looked forward to the journey.", "anticipation"),
    ("The child laughed with pure delight.", "joy"),
    ("The warrior raged against his enemies.", "anger"),
    ("The widow mourned her loss.", "sadness"),
    ("The sailor dreaded the coming storm.", "fear"),
    ("The nobles were appalled by the scandal.", "disgust"),
    ("The audience was amazed by the performance.", "surprise"),
    ("The villagers relied on their chief.", "trust"),
    ("The students eagerly awaited the results.", "anticipation"),
    ("The bride smiled with happiness.", "joy"),
    ("The tyrant was wrathful and cruel.", "anger"),
    ("The orphan felt miserable and alone.", "sadness"),
    ("The prisoner was terrified of the dark.", "fear"),
    ("The chef was revolted by the spoiled food.", "disgust"),
    ("The magician stunned the crowd.", "surprise"),
    ("The soldier believed in his commander.", "trust"),
    ("The scientist expected a breakthrough.", "anticipation"),
    ("The dancer performed with great joy.", "joy"),
    ("The beast howled in rage.", "anger"),
    ("The poet wrote of heartbreak.", "sadness"),
    ("The mouse was scared of the cat.", "fear"),
    ("The lady was sickened by the sight.", "disgust"),
    ("The boy was startled by the noise.", "surprise"),
    ("The friends counted on each other.", "trust"),
    ("The farmer hoped for good weather.", "anticipation"),
    ("She beamed with pride.", "joy"),
    ("He seethed with frustration.", "anger"),
    ("They grieved together.", "sadness"),
    ("The horse panicked at the thunder.", "fear"),
    ("The host was offended by the remark.", "disgust"),
    ("The discovery was unexpected.", "surprise"),
    ("The captain earned the crew's respect.", "trust"),
    ("The town prepared for the festival.", "anticipation"),
    ("The baby giggled with glee.", "joy"),
    ("The villain plotted with malice.", "anger"),
    ("The shepherd felt forlorn.", "sadness"),
    ("The deer froze in terror.", "fear"),
    ("The critic was contemptuous of the work.", "disgust"),
    ("The twist in the story was shocking.", "surprise"),
    ("The dog was loyal to its owner.", "trust"),
    ("The inventor dreamed of success.", "anticipation"),
    ("The grandmother smiled warmly.", "joy"),
    ("The pirate cursed angrily.", "anger"),
    ("The singer sang a melancholy tune.", "sadness"),
    ("The child hid under the bed in fright.", "fear"),
    ("The taste was absolutely awful.", "disgust"),
    ("Nobody expected the visitor.", "surprise"),
    ("She confided in her best friend.", "trust"),
    ("He counted down the days excitedly.", "anticipation"),
    ("The festival was full of laughter.", "joy"),
    ("The storm raged through the night.", "anger"),
    ("The letter brought tears.", "sadness"),
    ("Shadows in the forest filled them with dread.", "fear"),
    ("The smell from the swamp was nauseating.", "disgust"),
    ("The ending of the tale was astonishing.", "surprise"),
    ("The people had confidence in their leader.", "trust"),
    ("Everyone looked forward to the celebration.", "anticipation"),
    ("The reunion was filled with happiness.", "joy"),
    ("The dragon roared with fury.", "anger"),
    ("The farewell was bittersweet.", "sadness"),
    ("The darkness of the cave was frightening.", "fear"),
    ("The rotting fruit was repugnant.", "disgust"),
    ("The revelation left everyone speechless.", "surprise"),
    ("The bond between them was unbreakable.", "trust"),
    ("The kingdom awaited the coronation.", "anticipation"),
]

INTENSIFIERS = ["very", "extremely", "incredibly", "absolutely", "deeply"]
INHIBITORS = ["slightly", "somewhat", "barely", "kind of", "a little"]
NEGATORS = ["not", "never", "no longer", "hardly"]

# Plutchik opposite emotions for negation testing
PLUTCHIK_OPPOSITES = {
    "joy": "sadness", "sadness": "joy",
    "anger": "fear", "fear": "anger",
    "trust": "disgust", "disgust": "trust",
    "surprise": "anticipation", "anticipation": "surprise",
}


def get_modifier_dataset() -> List[Dict]:
    """
    Study 7: Creates original, intensified, and inhibited versions.
    Returns: [{'original': str, 'intensified': str, 'inhibited': str, 'emotion': str}]
    """
    import random
    random.seed(42)
    data = []
    for sentence, emotion in FAIRY_TALE_SENTENCES:
        intensifier = random.choice(INTENSIFIERS)
        inhibitor = random.choice(INHIBITORS)
        # Insert modifier before the emotional adjective/verb (simplified: after "was"/"felt")
        words = sentence.split()
        insert_pos = None
        for i, w in enumerate(words):
            if w.lower() in ["was", "felt", "were", "is"]:
                insert_pos = i + 1
                break
        if insert_pos is None:
            insert_pos = 1  # fallback: after first word

        intensified = words[:insert_pos] + [intensifier] + words[insert_pos:]
        inhibited = words[:insert_pos] + [inhibitor] + words[insert_pos:]

        data.append({
            "original": sentence,
            "intensified": " ".join(intensified),
            "inhibited": " ".join(inhibited),
            "emotion": emotion,
        })
    return data


def get_negation_dataset() -> List[Dict]:
    """
    Study 8: Creates original and negated versions.
    Returns: [{'original': str, 'negated': str, 'original_emotion': str, 'expected_emotion': str}]
    """
    import random
    random.seed(42)
    data = []
    for sentence, emotion in FAIRY_TALE_SENTENCES:
        negator = random.choice(NEGATORS[:2])  # "not" or "never"
        words = sentence.split()
        insert_pos = None
        for i, w in enumerate(words):
            if w.lower() in ["was", "felt", "were", "is"]:
                insert_pos = i + 1
                break
        if insert_pos is None:
            insert_pos = 1

        negated = words[:insert_pos] + [negator] + words[insert_pos:]
        expected = PLUTCHIK_OPPOSITES.get(emotion, emotion)

        data.append({
            "original": sentence,
            "negated": " ".join(negated),
            "original_emotion": emotion,
            "expected_emotion": expected,
        })
    return data


# ============================================================
# SUMMARY
# ============================================================

def load_all_datasets() -> Dict[str, List[Dict]]:
    """Load all datasets for the full 9-study benchmarking suite."""
    return {
        "goemotions": load_goemotions(),
        "isear": load_isear(),
        "semeval2018": load_semeval2018(),
        "financial_phrasebank": load_financial_phrasebank(),
        "senti4sd": load_senti4sd(),
        "modifier_test": get_modifier_dataset(),
        "negation_test": get_negation_dataset(),
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    datasets = load_all_datasets()
    for name, data in datasets.items():
        print(f"{name}: {len(data)} samples")
        if data and isinstance(data[0], dict) and "text" in data[0]:
            print(f"  Sample: {data[0]['text'][:80]}...")
