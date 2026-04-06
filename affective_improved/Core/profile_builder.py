import torch


from Core.get_nearest_neighbors import get_nearest_neighbours
from Core.modifier_handling import resolve_modifiers_and_negations, negations


# -------- MEAN POOLING --------
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


# -------- EMBEDDING --------
def get_mean_pooling_emb(sentences, tokenizer, model):
    device = next(model.parameters()).device

    encoded_input = tokenizer(
        sentences,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors='pt'
    ).to(device)

    with torch.no_grad():
        model_output = model(**encoded_input)

    return mean_pooling(model_output, encoded_input['attention_mask']).tolist()


# -------- MAIN --------
def build_profile(sentence, window_size, df, vocab_matrix, tokenizer, model, keyword_extraction, modifier_detection):

    sentence_tokens = sentence.lower().split()

    # -------- EMBEDDING --------
    sentence_emb = get_mean_pooling_emb([sentence], tokenizer, model)

    # -------- FAST NN --------
    neighbour_output = get_nearest_neighbours([sentence_emb[0]], df, vocab_matrix)
    normalized_score_dict = neighbour_output[0]

    # -------- MODIFIERS (SAFE) --------
    if modifier_detection:
        try:
            resolved_output = resolve_modifiers_and_negations(
                sentence_tokens,
                sentence_tokens,
                sentence_tokens,
                normalized_score_dict
            )
            normalized_score_dict = resolved_output[0]
        except:
            print("⚠️ modifier skipped")

    normalized_score_dict = dict(sorted(normalized_score_dict.items(), key=lambda x: x[1]))

    return [normalized_score_dict, []]