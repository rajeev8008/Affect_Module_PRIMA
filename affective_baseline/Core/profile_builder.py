import random
from datetime import datetime
import torch
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#Enable matplotlib to be interactive (zoom etc)
import ast

from Core.get_nearest_neighbors import get_nearest_neighbours
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


def get_mean_pooling_emb(sentences,tokenizer,model):
    number_of_gpu_cores = 1  # Fixed: User has 1 GPU (RTX 3050)
    gpu_core = random.randint(0, number_of_gpu_cores-1)
    device = "cuda:"+str(gpu_core) if torch.cuda.is_available() else "cpu"
    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=128, return_tensors='pt').to(device)
    # Compute token embeddings
    with torch.no_grad():
        model = model.to(device)
        model_output = model(**encoded_input)

    sentence_embeddings_raw = mean_pooling(model_output, encoded_input['attention_mask'])
    sentence_embeddings = sentence_embeddings_raw.tolist()

    return sentence_embeddings

#converting tokenizer embedded token id lists to human readable word lists
def convet_encordings_to_words(input_encodings,tokenizer):
    tokens = []
    for each_sent in input_encodings["input_ids"]:
        tokens.append(tokenizer.convert_ids_to_tokens(each_sent))
    return tokens


def optimized_kwd_extractor(sentence, tokenizer, model):
    print('optimized')
    print(sentence)
    device = "cuda:1" if torch.cuda.is_available() else "cpu"
    print(device)
    encoded_input = tokenizer(sentence, padding=True, truncation=True, max_length=128, return_tensors='pt').to(device)
    # Compute token embeddings
    print('enc_inp',encoded_input)
    with torch.no_grad():
        model = model.to(device)
        model_output = model(**encoded_input)

    sentence_embeddings_raw = mean_pooling(model_output, encoded_input['attention_mask'])
    sentence_embeddings = sentence_embeddings_raw.tolist()

    wp_tokens = convet_encordings_to_words(encoded_input,tokenizer)
    print(wp_tokens)


def build_profile(sentence ,window_size,df,tokenizer,model,keyword_extraction,modifier_detection):



    if(keyword_extraction):
        # optimized_kwd_extractor(sentence, tokenizer, model)
        sentence_tokens = sentence.split(' ')
        sentence_pieces = [sentence]
        for i in range(0, len(sentence_tokens) + 1 - window_size):
            sliding_piece = ' '.join(sentence_tokens[i: i + window_size])
            sentence_pieces.append(sliding_piece)

        sentence_emb = get_mean_pooling_emb(sentence_pieces, tokenizer, model)
        neighbour_output = get_nearest_neighbours([sentence_emb[0]], df)
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
        neighbour_output = get_nearest_neighbours([sentence_emb[0]], df)
        normalized_score_dict = neighbour_output[0]
        normalized_score_dict = {k: v for k, v in sorted(normalized_score_dict.items(), key=lambda item: item[1])}
        neighbour_dict = neighbour_output[1]
        fixed_top_windows = []

    return [normalized_score_dict,fixed_top_windows[:1]]


def plot_emotional_weight(x ,y):
    # plotting the points
    plt.figure(figsize=(20 ,5))
    plt.plot(x, y)

    # naming the x axis
    plt.xlabel('word windows')
    # naming the y axis
    plt.ylabel('emotional contribution')

    # giving a title to my graph
    # plt.title('Emotion contribution o')

    # function to show the plot

    plt.show()

def check_for_negations(top_candidates):
    neg = False
    for tsp in top_candidates:
        for each_p in tsp.split(' '):
            if(each_p in negations):
                # print('profiles are negated')
                neg = True
    return neg





# import ast
# tokenizer = AutoTokenizer.from_pretrained("E:\Projects\emo_detector_new\emo_bert_model")
# model = AutoModel.from_pretrained(r"E:\Projects\emo_detector_new\emo_bert_model")
#
#
# df = pd.read_csv(r"E:\Projects\emo_detector_new\vocabs\mean_pooling_emb_emobert_new_vocab_refined.csv")
# df = df.dropna()
# df['embedding'] = [ast.literal_eval(i) for i in df['embedding'].values.tolist()]

# print(emotion_candidates_recognition('Chefs not counting calories, study finds' ,1,df,tokenizer,model))

# {'fear': 0.022, 'surprise': 0.027, 'anticipation': 0.027, 'trust': 0.038, 'senerity': 0.038, 'distraction': 0.044, 'interest_vigilance': 0.087, 'boredom': 0.1, 'joy': 0.199, 'disgust': 0.211, 'sadness': 0.248}