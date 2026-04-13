def calculate_scores(neaarest_neighbs_words,neaarest_neighbs_labels):
  score_dict = {
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

  for i in range(0,len(neaarest_neighbs_words)):
    score = 50-i
    label = neaarest_neighbs_labels[i]
    # Map legacy labels to canonical 14 Plutchik labels
    label_map = {
        'senerity': 'serenity',
        'joy': 'joy_ecstasy',
        'sad': 'sadness',
        'surprise': 'amazement_surprise',
        'disgust': 'disgust_loathing',
    }
    label = label_map.get(label, label)
    if label in score_dict:
      score_dict[label] = score_dict[label] + score

  score_max = (len(neaarest_neighbs_words)*(len(neaarest_neighbs_words)-1))/2
  normalized_score_dict = score_dict.copy()
  for k in list(score_dict.keys()):
    if score_dict[k] == 0:
      del normalized_score_dict[k]
    else:
      normalized_score_dict[k] = round((score_dict[k]/score_max),3)

  return normalized_score_dict