import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

negations = ['never','not', 'no', 'didn', "didn't", 'didnt', 'didn t','doesn t', 'doesnt', "doesn't", "won't", 'won t', 'wont', "isn't","isnt","isn t", "aren't", 'aren t', 'arent', 'don t', "don't", 'dont',"haven't","haven t","havent",'weren t', "weren't", 'werent', "wasn't", 'wasn t', 'wasnt', 'wouldn t', "wouldn't", 'wouldnt', "can't", 'can t', 'couldn t',"couldn't", 'cant', 'cannot', 'couldnt', 'shouldnt', "shouldn't", 'shouldn t', 'neither', 'impossible', 'didn', 'wasn', 'weren', 'aren', 'don', 'doesn', 'couldn', 'shouldn', 'wouldn', 'won','nothing']

intensity_modifiers=['absolutely:B_INCR:0.9', 'almost:B_DECR:0.2', 'always:B_INCR:0.9', 'amazingly:B_INCR:0.8', 'awfully:B_INCR:0.8',
      'completely:B_INCR:0.9', 'considerable:B_INCR:0.6', 'considerably:B_INCR:0.6', 'decidedly:B_INCR:0.6', 'deeply:B_INCR:0.9',
      'effing:B_INCR:0.7', 'enormous:B_INCR:0.8', 'enormously:B_INCR:0.8', 'entirely:B_INCR:0.9', 'especially:B_INCR:0.8', 'exceptional:B_INCR:0.8',
      'exceptionally:B_INCR:0.8', 'extreme:B_INCR:0.9', 'extremely:B_INCR:0.9', 'fabulously:B_INCR:0.8', 'flippin:B_INCR:0.6', 'flipping:B_INCR:0.6',
      'frackin:B_INCR:0.6', 'fracking:B_INCR:0.6', 'frickin:B_INCR:0.7', 'fricking:B_INCR:0.7', 'friggin:B_INCR:0.7', 'frigging:B_INCR:0.7', 'fully:B_INCR:0.9',
      'greatly:B_INCR:0.8', 'hella:B_INCR:0.8','bloody:B_INCR:0.8', 'highly:B_INCR:0.9', 'hugely:B_INCR:0.9', 'incredible:B_INCR:0.9', 'incredibly:B_INCR:0.9', 'intensely:B_INCR:0.9',
      'just enough:B_DECR:0.4', 'kind of:B_DECR:0.3', 'kinda:B_DECR:0.3', 'kindof:B_DECR:0.3', 'kind-of:B_DECR:0.3', 'less:B_DECR:0.3', 'little:B_DECR:0.3', 'major:B_INCR:0.6',
      'majorly:B_INCR:0.6', 'marginal:B_DECR:0.3', 'marginally:B_DECR:0.3', 'more:B_INCR:0.6', 'most:B_INCR:0.8', 'not much:B_DECR:0.2', 'occasional:B_DECR:0.6',
      'occasionally:B_DECR:0.6', 'particularly:B_INCR:0.7', 'partly:B_DECR:0.3','partially:B_DECR:0.5', 'purely:B_INCR:0.9', 'quite:B_INCR:0.6', 'really:B_INCR:0.8', 'remarkably:B_INCR:0.9',
      'slight:B_DECR:0.3', 'slightly:B_DECR:0.6','barely:B_DECR:0.7', 'so:B_INCR:0.8', 'somewhat:B_DECR:0.4', 'soo:B_INCR:0.9', 'sort of:B_DECR:0.4', 'sorta:B_DECR:0.4', 'sortof:B_DECR:0.4',
      'sort-of:B_DECR:0.4', 'substantially:B_INCR:0.7', 'super:B_INCR:0.8', 'thoroughly:B_INCR:0.8', 'total:B_INCR:0.8', 'totally:B_INCR:0.9', 'tremendous:B_INCR:0.8',
      'tremendously:B_INCR:0.8', 'truly:B_INCR:0.9', 'unbelievably:B_INCR:0.9', 'unusually:B_INCR:0.7', 'utter:B_INCR:0.8', 'utterly:B_INCR:0.8', 'very:B_INCR:0.8',
      'not very:B_DECR:0.7']


def map_candidate_to_emotion(neighbour_dict, candidate_dict):
    # print(neighbour_dict)
    # print(len(neighbour_dict['words']))
    # print(candidate_dict)
    emo_candi_dict = {}
    neighbor_df = pd.DataFrame(neighbour_dict)
    # print(neighbor_df.head())

    dft = neighbor_df.groupby('labels')['words'].nunique().sort_values(ascending=False).reset_index(name='count')
    unique_emos = dft['labels'][:3]
    # print(unique_emos)

    for each_cd in candidate_dict:
        dis_emo_dict = {}
        for each_ue in unique_emos:
            dis_list = []
            emod = neighbor_df.loc[neighbor_df['labels'] == each_ue][:50]
            for j, e_row in emod.iterrows():
                dis_list.append(cosine_similarity([e_row['embs']], [each_cd[2]]))
            # print(np.mean(dis_list))
            dis_emo_dict[each_ue] = np.mean(dis_list)
        # print(each_cd[0])
        # print(dis_emo_dict)
        # print(max(dis_emo_dict, key=dis_emo_dict.get))
        emo_candi_dict[each_cd[0]]:max(dis_emo_dict, key=dis_emo_dict.get)
        # break
    return emo_candi_dict


def fix_score(current_score,in_dc,in_sc):
  if(in_dc=='B_INCR'):
    final_score = current_score+(current_score*in_sc)
  elif(in_dc=='B_DECR'):
    final_score = current_score-(current_score*in_sc)
  return final_score

def check_for_negations(top_candidates):
  neg = False
  for tsp in top_candidates:
    for each_p in tsp.split(' '):
      if(each_p in negations):
        # print('profiles are negated')
        neg = True
  return neg


def map_opposite_emotions(emo_dict):
      opposite_emotions = {'anticipation': 'amazement_surprise',
                         'anger': 'joy_ecstasy',
                         'fear': 'trust',
                         'sadness': 'joy_ecstasy',
                         'trust': 'fear',
                         'serenity': 'distraction',
                         'joy_ecstasy': 'sadness',
                         'admire': 'disgust_loathing',
                         'acceptance': 'disgust_loathing',
                         'amazement_surprise': 'anticipation',
                         'distraction': 'serenity',
                         'boredom': 'interest_vigilance',
                         'disgust_loathing': 'joy_ecstasy',
                         'interest_vigilance': 'boredom'
                         }
      opposed_dict = {}

      for each_key in emo_dict.keys():
        opposite_emo = opposite_emotions[each_key]
        if(opposite_emo in opposed_dict):
          opposed_dict[opposite_emo] = opposed_dict[opposite_emo]+emo_dict[each_key]
        else:
          opposed_dict[opposite_emo] = emo_dict[each_key]

      # print(opposed_dict)

      return opposed_dict


def resolve_modifiers_and_negations(top_windows,sentence_tokens,emo_candidates,normalized_score_dict ):
    normalized_score_dict = {k: v for k, v in sorted(normalized_score_dict.items(), key=lambda item: item[1])}
    fixed_top_windows = []
    for i, emoWord in enumerate(top_windows):
        # Safe positional search: handle multi-word windows and duplicates
        end_ind_int = -1
        emo_words = emoWord.split(' ')
        if len(emo_words) == 1:
            # Single word: find first occurrence
            for idx, tok in enumerate(sentence_tokens):
                if tok.lower() == emoWord.lower():
                    end_ind_int = idx
                    break
        else:
            # Multi-word: find the position of the last word in the window
            for idx in range(len(sentence_tokens) - len(emo_words) + 1):
                window = ' '.join(sentence_tokens[idx:idx+len(emo_words)])
                if window.lower() == emoWord.lower():
                    end_ind_int = idx + len(emo_words) - 1
                    break
        if end_ind_int == -1:
            # Word not found — skip modifier detection for this window
            fixed_top_windows.append(emoWord.lower())
            continue
        start_ind_int = max(0, end_ind_int - 3)
        text_chunk_int = (' ').join(sentence_tokens[start_ind_int:end_ind_int])
        text_chunk_int = text_chunk_int.strip().lower()
        fixed_top_windows.append(text_chunk_int)

        # check_negations and intensity modifiers only in top candidate
        if (i == 0):

            # check for intensifiers or inhibitors
            for im in intensity_modifiers:
                im_splits = im.split(':')
                int_w = im_splits[0]
                in_dc = im_splits[1]
                in_sc = float(im_splits[2])
                if (len(int_w.split()) == 1):
                    if int_w in text_chunk_int.split():
                        crnt_sc = normalized_score_dict[list(normalized_score_dict.keys())[-1]]
                        normalized_score_dict[list(normalized_score_dict.keys())[-1]] = fix_score(crnt_sc, in_dc, in_sc)
                elif (len(int_w.split()) > 1):
                    if int_w in text_chunk_int:
                        crnt_sc = normalized_score_dict[list(normalized_score_dict.keys())[-1]]
                        normalized_score_dict[list(normalized_score_dict.keys())[-1]] = fix_score(crnt_sc, in_dc, in_sc)

            # check negations
            if (check_for_negations([text_chunk_int])):
                normalized_score_dict = map_opposite_emotions(normalized_score_dict)

    intensity_sum = 0
    for e_key in list(normalized_score_dict.keys()):
        intensity_sum=intensity_sum+normalized_score_dict[e_key]
    for e_key in list(normalized_score_dict.keys()):
        if(intensity_sum!=0):
            normalized_score_dict[e_key] = round((normalized_score_dict[e_key]/intensity_sum),3)
    return [normalized_score_dict,top_windows]