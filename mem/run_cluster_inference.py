import os
import json
import torch
import pandas as pd
import ast
import time
from transformers import AutoTokenizer, AutoModel
import sys

# Add affective_improved to sys.path to import Core
sys.path.append(os.path.join(os.getcwd(), 'affective_improved'))

from Core.profile_builder import build_profile, get_mean_pooling_emb
from Core.get_nearest_neighbors import build_vocab_matrix

def run_inference(input_file, output_file):
    print(f"Loading model and lexicon...")
    model_path = "joeddav/distilbert-base-uncased-go-emotions-student"
    base_dir = os.path.join(os.getcwd(), 'affective_improved')
    vocab_path = os.path.join(base_dir, "Vocabularies", "goemotion_vocabulary.csv")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModel.from_pretrained(model_path).to(device)

    df = pd.read_csv(vocab_path)
    df = df.dropna()
    df['embedding'] = [ast.literal_eval(i) for i in df['embedding'].values.tolist()]
    vocab_matrix = build_vocab_matrix(df)

    print(f"Loading clusters from {input_file}...")
    with open(input_file, 'r') as f:
        clusters = json.load(f)

    results = []
    total = len(clusters)
    
    start_time = time.time()
    for i, text in enumerate(clusters):
        print(f"[{i+1}/{total}] Processing Cluster...")
        
        # Get emotion scores (improved version)
        pred = build_profile(text, 1, df, tokenizer, model, 
                             keyword_extraction=True, modifier_detection=True,
                             vocab_matrix=vocab_matrix)
        
        emotion_scores = pred[0]
        
        # Get top 5 dominant emotions
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
        dominant_emotions = {k: round(float(v), 3) for k, v in sorted_emotions[:5]}
        
        # Get vector embedding (mean pooled)
        embedding = get_mean_pooling_emb([text], tokenizer, model)[0]
        
        results.append({
            "cluster_id": i + 1,
            "raw_text": text,
            "dominant_emotions": dominant_emotions,
            "vector_embedding": embedding
        })

    end_time = time.time()
    print(f"Inference completed in {end_time - start_time:.2f} seconds.")

    print(f"Saving outputs to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    print("Done!")

if __name__ == "__main__":
    input_file = "final_9_clusters_only.json"
    output_file = "final_9_clusters_affect.json"
    run_inference(input_file, output_file)
