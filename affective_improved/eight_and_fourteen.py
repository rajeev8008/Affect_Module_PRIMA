import nltk as nltk
import pandas as pd
from transformers import AutoTokenizer, AutoModel
from Core.profile_builder import build_profile
import ast


model_path = r"E:\Projects\Emotion_work_Gihan\Emo_LexiBERTa\Finetuned_Langue_Models\DistilBERT_GoEmotions_Finetuned"
vocab_path = r"E:\Projects\Emotion_work_Gihan\Emo_LexiBERTa\Vocabularies\goemotion_vocabulary.csv"


def ft_to_et(emo_dict):

    eight_dict = {'sadness': 0, 'anger': 0, 'joy': 0, 'anticipation': 0, 'fear': 0, 'surprise': 0, 'disgust': 0,
                  'trust': 0}

    if ('anticipation' in emo_dict.keys()):
        eight_dict['anticipation'] += emo_dict['anticipation']
    if ('amazement_surprise' in emo_dict.keys()):
        eight_dict['surprise'] += emo_dict['amazement_surprise']
    if ('distraction' in emo_dict.keys()):
        eight_dict['surprise'] += emo_dict['distraction']
    if ('fear' in emo_dict.keys()):
        eight_dict['fear'] += emo_dict['fear']
    if ('trust' in emo_dict.keys()):
        eight_dict['trust'] += emo_dict['trust']
    if ('interest_vigilance' in emo_dict.keys()):
        eight_dict['anticipation'] += emo_dict['interest_vigilance']
    if ('anger' in emo_dict.keys()):
        eight_dict['anger'] += emo_dict['anger']
    if ('disgust_loathing' in emo_dict.keys()):
        eight_dict['disgust'] += emo_dict['disgust_loathing']
    if ('senerity' in emo_dict.keys()):
        eight_dict['joy'] += emo_dict['senerity']
    if ('boredom' in emo_dict.keys()):
        eight_dict['disgust'] += emo_dict['boredom']
    if ('acceptance' in emo_dict.keys()):
        eight_dict['trust'] += emo_dict['acceptance']
    if ('joy_ecstasy' in emo_dict.keys()):
        eight_dict['joy'] += emo_dict['joy_ecstasy']
    if ('admire' in emo_dict.keys()):
        eight_dict['trust'] += emo_dict['admire']
    if ('sadness' in emo_dict.keys()):
        eight_dict['sadness'] += emo_dict['sadness']

    # print(eight_dict)
    return eight_dict


if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModel.from_pretrained(model_path)


    df = pd.read_csv(vocab_path)
    df = df.dropna()
    df['embedding'] = [ast.literal_eval(i) for i in df['embedding'].values.tolist()]

    sentence = "People were confused after the unexpected news"
    # sentence = "it was a terrible memory"
    # sentence = "I am sure that he is a good person"
    pred = build_profile(sentence,1,df,tokenizer,model,keyword_extraction=True,modifier_detection=True)
    print(pred[0])
    print('eight prof')
    e_pr = ft_to_et(pred[0])
    print(e_pr)

    # sentence = "muslims are extremely friendly"
    # pred = build_profile(sentence, 1, df, tokenizer, model, keyword_extraction=True, modifier_detection=True)
    # print(pred)
    # print('eight prof')
    # e_pr = ft_to_et(pred[0])
    # print(e_pr)
    #