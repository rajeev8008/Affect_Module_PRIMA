import pandas as pd
from transformers import AutoTokenizer, AutoModel
from transformers import DistilBertTokenizerFast
from Core.profile_builder import build_profile
import ast
import numpy as np

model_path = r"E:\Projects\Emo_LexiBERTa\Finetuned_Langue_Models\DistilBERT_GoEmotions_Finetuned"
vocab_path = r"E:\Projects\Emo_LexiBERTa\Vocabularies\goemotion_vocabulary.csv"

number_of_chunks = 3

tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)

df = pd.read_csv(vocab_path)
df = df.dropna()
df['embedding'] = [ast.literal_eval(i) for i in df['embedding'].values.tolist()]



df_large = pd.read_csv(r"E:\Projects\DSI Gihan Prev\us_election_experiments\results\processed_trump_biden_all_maxes.csv")
print(len(df_large))
chunks = np.array_split(df_large, number_of_chunks)
for itr,dff in enumerate(chunks):
    print(dff.head())
    print(len(dff),itr)
    profiles = []
    kwds = []

    for i,row in dff.iterrows():
        # print(row['text'])
        print([i,len(dff)])
        sentence = row['text']
        pred = build_profile(sentence, 1, df, tokenizer, model, keyword_extraction=True, modifier_detection=True)
        profiles.append(pred[0])
        kwds.append(pred[1])

    print(profiles)
    print(kwds)

    dff['emo_profiles'] = profiles
    dff['emo_kwds'] = kwds

    dff.to_csv(r"E:\Projects\EmoLexiBerta_Gihan\Emo_LexiBERTa\use_case_DSI\processed_trump_biden_all_maxes_with_emo_chunk_"+str(itr)+".csv")