import os
import nltk
import pandas as pd
from transformers import AutoTokenizer, AutoModel
from Core.profile_builder import build_profile
from Core.get_nearest_neighbors import build_vocab_matrix
import ast
import torch
import time


# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = "joeddav/distilbert-base-uncased-go-emotions-student"
vocab_path = os.path.join(BASE_DIR, "Vocabularies", "goemotion_vocabulary.csv")


def emo_detect_document(text, df, vocab_matrix, tokenizer, model):
    """Detect emotions across all sentences in a document."""
    output_emo_dict = {
              'anticipation':0,
              'anger':0,
              'fear':0,
              'sadness':0,
              'trust':0,
              'serenity':0,
              'joy_ecstasy':0,
              'admire':0,
              'acceptance':0,
              'amazement_surprise':0,
              'distraction':0,
              'boredom':0,
              'disgust_loathing':0,
              'interest_vigilance':0}
    a_list = nltk.tokenize.sent_tokenize(text)

    for each_s in a_list:
        pred = build_profile(each_s, 1, df, tokenizer, model,
                             keyword_extraction=True, modifier_detection=True,
                             vocab_matrix=vocab_matrix)
        for each_k in pred[0].keys():
            if each_k in output_emo_dict:
                output_emo_dict[each_k] = output_emo_dict[each_k] + pred[0][each_k]

    return output_emo_dict


if __name__ == "__main__":
    print("=" * 60)
    print("PRIMA Affective Component - Improved Version")
    print("=" * 60)
    print("Loading model and lexicon...")

    # ---------------- DEVICE ----------------
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModel.from_pretrained(model_path).to(device)

    df = pd.read_csv(vocab_path)
    df = df.dropna()
    df['embedding'] = [ast.literal_eval(i) for i in df['embedding'].values.tolist()]

    # Build normalised vocab matrix once for fast NN search
    vocab_matrix = build_vocab_matrix(df)

    print(f"✓ Model loaded: DistilBERT + GoEmotions")
    print(f"✓ Lexicon loaded: {len(df)} Plutchik emotion terms")
    print(f"✓ Vocab matrix built (fast retrieval enabled)")
    print(f"✓ Using device: {device}")
    print("=" * 60)
    print("\nEnter text to detect emotions (or 'quit' to exit)\n")

    while True:
        # Get user input
        sentence = input(">>> ").strip()

        # Exit condition
        if sentence.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break

        # Skip empty input
        if not sentence:
            continue

        # Detect emotions
        try:
            start_time = time.time()

            pred = build_profile(sentence, 1, df, tokenizer, model,
                               keyword_extraction=True, modifier_detection=True,
                               vocab_matrix=vocab_matrix)

            end_time = time.time()
            processing_time = end_time - start_time

            # Display results
            print("\n" + "-" * 60)
            print("Emotion Scores:")
            emotion_scores = pred[0]
            keywords = pred[1]

            # Sort by score (descending)
            sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)

            # Display top 5 emotions
            for emotion, score in sorted_emotions[:5]:
                bar = "█" * int(score * 50)
                print(f"  {emotion:20s} {score:.3f} {bar}")

            # Display keywords
            if keywords:
                print(f"\nKeywords: {', '.join(keywords)}")

            print(f"\nProcessing time: {processing_time:.3f}s")
            print("-" * 60 + "\n")

        except Exception as e:
            print(f"\n❌ Error: {e}\n")