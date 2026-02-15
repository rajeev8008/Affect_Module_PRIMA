def calculate_scores(neaarest_neighbs_words,neaarest_neighbs_labels):
  score_dict = {
      'negative': 0,
      'positive': 0,
      'uncertainty': 0,
      'litigious': 0,
      'model_strong': 0,
      'model_weak': 0,
              'anticipation':0,
              'anger':0,
              'fear':0,
              'sadness':0,
              'trust':0,
              'senerity':0,
              'joy_ecstasy':0,
              'joy':0,
              'sad':0,
              'admire':0,
              'acceptance':0,
              'amazement_surprise':0,
              'surprise':0,
              'distraction':0,
              'boredom':0,
              'disgust_loathing':0,
              'disgust':0,
              'interest_vigilance':0}

  for i in range(0,len(neaarest_neighbs_words)):
    score = 50-i
    # print(score,neaarest_neighbs_words[i],neaarest_neighbs_labels[i])
    score_dict[neaarest_neighbs_labels[i]]=score_dict[neaarest_neighbs_labels[i]]+score

  score_max = (len(neaarest_neighbs_words)*(len(neaarest_neighbs_words)-1))/2
  normalized_score_dict = score_dict.copy()
  for k in score_dict.keys():
    if score_dict[k] ==0:
      del normalized_score_dict[k]
    else:
      normalized_score_dict[k] = round((score_dict[k]/score_max),3)

  # print(score_dict)
  print(normalized_score_dict)

  return normalized_score_dict