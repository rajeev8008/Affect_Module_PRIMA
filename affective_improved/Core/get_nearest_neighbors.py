import numpy as np
from datetime import datetime
from Core.scoring import calculate_scores


def build_vocab_matrix(df):
    matrix = np.array(df['embedding'].tolist(), dtype='float32')
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1e-9, norms)
    return matrix / norms


def get_nearest_neighbours(embedding, df, vocab_matrix, top_k=50):

    t1 = datetime.now()

    query = np.array(embedding[0], dtype='float32')
    norm = np.linalg.norm(query)
    if norm > 0:
        query = query / norm

    scores = vocab_matrix @ query

    if len(scores) <= top_k:
        top_idx = np.argsort(scores)[::-1]
    else:
        top_idx = np.argpartition(scores, -top_k)[-top_k:]
        top_idx = top_idx[np.argsort(scores[top_idx])[::-1]]

    rows = df.iloc[top_idx]

    words = rows['token'].tolist()
    labels = rows['fourteen_label'].tolist()
    embs = vocab_matrix[top_idx].tolist()

    n_score_dict = calculate_scores(words, labels)

    t2 = datetime.now()
    print("time nn and score", t2 - t1)

    return [n_score_dict, {"words": words, "embs": embs, "labels": labels}]