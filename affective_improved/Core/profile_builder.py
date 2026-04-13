from datetime import datetime
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from Core.get_nearest_neighbors import get_nearest_neighbours, build_vocab_matrix
from Core.modifier_handling import map_opposite_emotions, negations, map_candidate_to_emotion, \
    resolve_modifiers_and_negations
from Core.scoring import calculate_scores

# df = pd.read_csv(r'E:\Projects\emo_detector_new\vocabs\mean_pooling_emb_emobert_new_vocab_refined.csv')
# # print(df.head())
# # print(df.columns)
# df = df.dropna()



#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    # print('ime',input_mask_expanded)
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    # print('se',sum_embeddings)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask


def get_mean_pooling_emb(sentences, tokenizer, model):
    """Encode *sentences* via mean-pooled BERT embeddings.

    Automatically uses the device the model is already on.
    """
    device = next(model.parameters()).device
    encoded_input = tokenizer(
        sentences, padding=True, truncation=True, max_length=128, return_tensors='pt'
    ).to(device)
    with torch.no_grad():
        model_output = model(**encoded_input)

    return mean_pooling(model_output, encoded_input['attention_mask']).tolist()




def build_profile(sentence, window_size, df, tokenizer, model, keyword_extraction, modifier_detection, vocab_matrix=None):



    if(keyword_extraction):
        # optimized_kwd_extractor(sentence, tokenizer, model)
        sentence_tokens = sentence.split(' ')
        sentence_pieces = [sentence]
        for i in range(0, len(sentence_tokens) + 1 - window_size):
            sliding_piece = ' '.join(sentence_tokens[i: i + window_size])
            sentence_pieces.append(sliding_piece)

        sentence_emb = get_mean_pooling_emb(sentence_pieces, tokenizer, model)
        neighbour_output = get_nearest_neighbours([sentence_emb[0]], df, vocab_matrix=vocab_matrix)
        normalized_score_dict = neighbour_output[0]
        neighbour_dict = neighbour_output[1]
        fixed_top_windows = []


        tuples = []
        for i in range(1, len(sentence_emb)):
            sliding_piece = sentence_pieces[i]
            dis = cosine_similarity([sentence_emb[i]], [sentence_emb[0]])
            # print(dis)
            tuples.append([sliding_piece, dis, sentence_emb[i]])
        # print([i[0] for i in tuples])
        # print([i[1].tolist()[0] for i in tuples])

        s_tup = sorted(tuples, key=lambda x: x[1])  # sort tuples based on the cosine distance
        # for kk in s_tup[::-1][:5]:
        #   print(kk)
        candidate_dict = s_tup[::-1][:5]
        print('*********')


        # emo_candidates = map_candidate_to_theme(neighbour_dict, candidate_dict)
        # print(emo_candidates)
        # print('*********')
        # print(emo_candidates)
        emo_candidates = [i[0] for i in candidate_dict]

        top_5_windows = [i for i in emo_candidates]
        # print('top', top_5_windows)
        fixed_top_windows = emo_candidates
        if(modifier_detection):


            # intensity modifiers/negations detection

            top_windows = top_5_windows
            resolved_output = resolve_modifiers_and_negations(top_windows, sentence_tokens, emo_candidates, normalized_score_dict)


            normalized_score_dict = resolved_output[0]
            fixed_top_windows = resolved_output[1]

            # print('fixed',fixed_top_windows)

            normalized_score_dict = {k: v for k, v in sorted(normalized_score_dict.items(), key=lambda item: item[1])}

    else:
        sentence_tokens = sentence.split(' ')
        sentence_pieces = [sentence]

        sentence_emb = get_mean_pooling_emb(sentence_pieces, tokenizer, model)
        neighbour_output = get_nearest_neighbours([sentence_emb[0]], df, vocab_matrix=vocab_matrix)
        normalized_score_dict = neighbour_output[0]
        normalized_score_dict = {k: v for k, v in sorted(normalized_score_dict.items(), key=lambda item: item[1])}
        neighbour_dict = neighbour_output[1]
        fixed_top_windows = []

    return [normalized_score_dict,fixed_top_windows[:1]]
