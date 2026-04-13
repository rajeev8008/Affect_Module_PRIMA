import numpy as np
from datetime import datetime
from Core.scoring import calculate_scores


def build_vocab_matrix(df):
    """Pre-compute a normalized embedding matrix for fast cosine similarity.

    Call this once at startup and pass the result to get_nearest_neighbours.
    """
    matrix = np.array(df['embedding'].tolist(), dtype='float32')
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1e-9, norms)
    return matrix / norms


def get_nearest_neighbours(embedding, df, vocab_matrix=None, top_k=50):
    """Return emotion scores and top-k nearest neighbours for *embedding*.

    When *vocab_matrix* is provided (pre-normalised matrix from
    ``build_vocab_matrix``), a single matrix–vector multiply replaces the old
    row-by-row loop, giving ~10-50× speedup.

    Falls back to the original iterative method when *vocab_matrix* is None so
    that callers that haven't been updated yet still work.
    """
    t1 = datetime.now()

    if vocab_matrix is not None:
        # ---- FAST PATH: vectorised cosine similarity ----
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

        neaarest_neighbs_words = rows['token'].tolist()
        neaarest_neighbs_labels = rows['fourteen_label'].tolist()
        neaarest_neighbs_embs = vocab_matrix[top_idx].tolist()
    else:
        # ---- LEGACY PATH: row-by-row (kept for backward compat) ----
        from sklearn.metrics.pairwise import cosine_similarity

        tuples = []
        for i, row_e in df.iterrows():
            dis = cosine_similarity([row_e['embedding']], embedding)
            tuples.append([row_e['token'], row_e['fourteen_label'], dis, row_e['embedding']])

        s_tup = sorted(tuples, key=lambda x: x[2])
        neaarest_neighbs_words = []
        neaarest_neighbs_embs = []
        neaarest_neighbs_labels = []
        for i, m in enumerate(s_tup[::-1]):
            if i < top_k:
                neaarest_neighbs_words.append(m[0])
                neaarest_neighbs_embs.append(m[3])
                neaarest_neighbs_labels.append(m[1])

    n_score_dict = calculate_scores(neaarest_neighbs_words, neaarest_neighbs_labels)

    t2 = datetime.now()
    print('time nn and score', t2 - t1)

    return [n_score_dict, {'words': neaarest_neighbs_words, 'embs': neaarest_neighbs_embs, 'labels': neaarest_neighbs_labels}]