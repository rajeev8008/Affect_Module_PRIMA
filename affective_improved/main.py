import os
import nltk
import pandas as pd
from transformers import AutoTokenizer, AutoModel
from Core.profile_builder import build_profile
from Core.get_nearest_neighbors import build_vocab_matrix   # 🔥 IMPORTANT
import ast
import torch
import time

# ---------------- PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = "joeddav/distilbert-base-uncased-go-emotions-student"
vocab_path = os.path.join(BASE_DIR, "Vocabularies", "goemotion_vocabulary.csv")

# ---------------- DEVICE ----------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------- LOAD ----------------
print("=" * 60)
print("PRIMA Affective Component - Improved Version")
print("=" * 60)
print("Loading model and lexicon...")

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path).to(device)   # ❌ removed attention (as you wanted)

df = pd.read_csv(vocab_path)
df = df.dropna()
df['embedding'] = [ast.literal_eval(i) for i in df['embedding'].values.tolist()]

# 🔥 BUILD MATRIX ONCE (VERY IMPORTANT)
vocab_matrix = build_vocab_matrix(df)

print("✓ Model loaded: DistilBERT + GoEmotions")
print("✓ Lexicon loaded")
print("✓ Vocab matrix built (fast retrieval enabled)")
print(f"✓ Using device: {device}")
print("=" * 60)

# ---------------- TEST INPUT ----------------
test_sentences = [
    "I feel very happy and excited today!",
    "I am really scared and nervous about my exam",
    "This is absolutely disgusting and annoying",
    "I love this so much, it's amazing!",
    "I feel bored and distracted right now"
]

# ---------------- RUN ----------------
for sentence in test_sentences:
    print("\n" + "=" * 60)
    print(f"Input: {sentence}")

    try:
        start = time.time()

        # ✅ FIXED CALL
        pred = build_profile(
            sentence,
            1,
            df,
            vocab_matrix,   # 🔥 NEW PARAM
            tokenizer,
            model,
            keyword_extraction=True,
            modifier_detection=True
        )

        end = time.time()

        emotion_scores = pred[0]

        print("\nTop Emotions:")

        sorted_emotions = sorted(emotion_scores.items(),
                                 key=lambda x: x[1],
                                 reverse=True)

        for emotion, score in sorted_emotions[:5]:
            bar = "█" * int(score * 50)
            print(f"  {emotion:20s} {score:.3f} {bar}")

        print(f"\nTime: {end - start:.3f}s")

    except Exception as e:
        print(f"\n❌ Error: {e}")