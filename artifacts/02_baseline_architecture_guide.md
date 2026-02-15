# PRIMA Affective Baseline - Architecture & File Guide

## Overview
The PRIMA Affective Component baseline implements the AWARE (Affective Word-level Association-based Retrieval) framework for detecting emotions from text using a retrieval-based approach with transformer embeddings.

**Current Configuration:**
- **Emotions**: 14 Plutchik emotions (full AWARE architecture)
- **Lexicon**: 1,193 emotion terms with pre-computed embeddings
- **Model**: DistilBERT fine-tuned on GoEmotions dataset
- **Processing Time**: ~730ms per sentence

---

## File Structure & Relationships

```
affective_baseline/
├── main.py                          # Entry point & orchestrator
├── requirements.txt                 # Python dependencies
├── README.md                        # Baseline documentation
│
├── Core/                            # Core emotion detection pipeline
│   ├── profile_builder.py          # Main pipeline orchestrator
│   ├── get_nearest_neighbors.py    # Similarity search
│   ├── scoring.py                  # Weighted scoring
│   └── modifier_handling.py        # Negation & intensifier handling
│
├── Vocabularies/                    # Emotion lexicons
│   ├── goemotion_vocabulary.csv    # 14-emotion lexicon (ACTIVE)
│   ├── plutchik_with_emobert_vocab.csv  # 8-emotion lexicon
│   └── lnm_vocab_even.csv          # Experimental
│
├── Building_Embedding_Space/       # Lexicon construction scripts
│   ├── lexicon_construction.py     # Build vocabulary from seed words
│   └── visualize_embedding_space.py  # Visualize emotion clusters
│
└── Finetuned_Langue_Models/        # Pre-trained model cache
    └── (Downloaded from HuggingFace on first run)
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      main.py (Orchestrator)                      │
│  1. Load model & tokenizer (DistilBERT)                         │
│  2. Load lexicon CSV (goemotion_vocabulary.csv)                 │
│  3. Parse embeddings from strings to arrays                     │
│  4. Enter interactive input loop                                │
└────────────┬────────────────────────────────────────────────────┘
             │
             ├─ User Input: "I have a presentation tomorrow"
             │
             v
┌─────────────────────────────────────────────────────────────────┐
│              profile_builder.py (Core Pipeline)                  │
│                                                                  │
│  STEP 1: Tokenization & Encoding                                │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ • Tokenize input (max 128 tokens)                      │    │
│  │ • Pass through DistilBERT (6 layers, 768-dim)          │    │
│  │ • Mean pooling → 768-dim sentence embedding            │    │
│  └────────────────────────────────────────────────────────┘    │
│                           │                                      │
│  STEP 2: Keyword Extraction                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ • Sliding window (n-grams, window_size=1)              │    │
│  │ • Compute cosine similarity each window vs full text   │    │
│  │ • Select top-5 most similar windows                    │    │
│  │ • Generate embeddings for each window                  │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────┬────────────────────────────────────────────────────┘
             │
             v
┌─────────────────────────────────────────────────────────────────┐
│          get_nearest_neighbors.py (Similarity Search)            │
│                                                                  │
│  For each keyword window embedding:                             │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ • Compute cosine similarity with ALL 1,193 lexicon     │    │
│  │   term embeddings (O(n) = ~100ms)                      │    │
│  │ • Sort by similarity (descending)                      │    │
│  │ • Select Top-50 nearest neighbors                      │    │
│  │ • Return: words, embeddings, emotion labels            │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────┬────────────────────────────────────────────────────┘
             │
             v
┌─────────────────────────────────────────────────────────────────┐
│                 scoring.py (Weighted Scoring)                    │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ • Assign scores: Rank 1 = 50 points, Rank 50 = 0       │    │
│  │ • Aggregate by emotion label (14 categories)           │    │
│  │ • Normalize: score / score_max where                   │    │
│  │   score_max = n*(n-1)/2                                │    │
│  │ • Remove zero-score emotions                           │    │
│  └────────────────────────────────────────────────────────┘    │
│                           │                                      │
│                 Initial Emotion Profile                         │
│         {fear: 0.105, anticipation: 0.320, joy: 0.441}          │
└────────────┬────────────────────────────────────────────────────┘
             │
             v
┌─────────────────────────────────────────────────────────────────┐
│         modifier_handling.py (Contextual Refinement)             │
│                                                                  │
│  STEP 1: Detect Modifiers                                       │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ • Check for 80+ intensifiers                           │    │
│  │   (very, extremely, really, so, etc.)                  │    │
│  │ • Boost dominant emotion by modifier weight            │    │
│  │   Example: "very happy" → joy * 1.8                    │    │
│  └────────────────────────────────────────────────────────┘    │
│                           │                                      │
│  STEP 2: Detect Negations                                       │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ • Check for 50+ negation terms                         │    │
│  │   (not, never, no, can't, won't, etc.)                 │    │
│  │ • Flip to opposite emotion on Plutchik wheel:          │    │
│  │   joy ↔ sadness, anger ↔ fear, trust ↔ disgust         │    │
│  └────────────────────────────────────────────────────────┘    │
│                           │                                      │
│  STEP 3: Re-normalize Scores                                    │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ • Ensure sum = 1.0                                      │    │
│  │ • Return final emotion profile                         │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────┬────────────────────────────────────────────────────┘
             │
             v
┌─────────────────────────────────────────────────────────────────┐
│                    Final Output (main.py)                        │
│                                                                  │
│  Emotion Scores:                                                │
│    fear                  0.402 ████████████████████              │
│    anticipation          0.225 ███████████                       │
│    trust                 0.158 ███████                           │
│                                                                  │
│  Keywords: presentation, tomorrow                               │
│  Processing time: 0.637s                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Dependencies

### main.py
**Imports:**
- `transformers` → AutoTokenizer, AutoModel
- `pandas` → Load CSV lexicon
- `Core.profile_builder` → build_profile()

**Role:** Entry point, loads model/lexicon, handles user I/O

---

### Core/profile_builder.py
**Imports:**
- `transformers` → Model inference
- `sklearn.metrics.pairwise` → Cosine similarity
- `Core.get_nearest_neighbors` → get_nearest_neighbours()
- `Core.modifier_handling` → resolve_modifiers_and_negations()

**Key Functions:**
- `mean_pooling()` → Compute sentence embedding
- `get_mean_pooling_emb()` → Encode text to 768-dim vector
- `optimized_kwd_extractor()` → Sliding window keyword extraction
- `build_profile()` → **Main pipeline orchestrator**

---

### Core/get_nearest_neighbors.py
**Imports:**
- `sklearn.metrics.pairwise` → Cosine similarity
- `Core.scoring` → calculate_scores()

**Key Functions:**
- `get_nearest_neighbours()` → Find top-50 similar terms from lexicon

**Algorithm:**
```python
for each lexicon_term in 1,193 terms:
    similarity = cosine_similarity(input_embedding, lexicon_embedding)
    tuples.append((word, emotion_label, similarity))

sort(tuples, descending)
return top_50
```

---

### Core/scoring.py
**Imports:** None (pure Python)

**Key Functions:**
- `calculate_scores()` → Rank-based weighted scoring

**Algorithm:**
```python
for rank in [1..50]:
    score = 50 - rank
    emotion_scores[label] += score

normalize(emotion_scores)
```

---

### Core/modifier_handling.py
**Imports:**
- `sklearn.metrics.pairwise` → Cosine similarity (for advanced features)

**Key Functions:**
- `resolve_modifiers_and_negations()` → Apply rule-based adjustments
- `map_opposite_emotions()` → Plutchik wheel emotion flipping
- `fix_score()` → Adjust scores based on intensifiers

**Data:**
- `intensity_modifiers` → 80+ terms with strength values
- Plutchik opposites mapping

---

## Key Design Decisions

### 1. Why Retrieval-Based (not Classification)?
- **Explainability**: Can trace which words influenced emotion scores
- **Flexibility**: Works with any emotion taxonomy (just change lexicon)
- **No retraining**: Add new emotions without model fine-tuning

### 2. Why DistilBERT?
- Smaller (66M params vs 110M)
- Faster inference (~500ms vs ~1s)
- Still captures semantic meaning effectively

### 3. Why Top-50 Neighbors?
- Balance between coverage and noise
- Empirically found to be optimal (AWARE paper experiments)

### 4. Why Weighted Scoring?
- Closer neighbors = more important
- Linear decay prevents over-weighting distant matches

---

## Performance Characteristics

| **Component** | **Time** | **Complexity** |
|--------------|----------|----------------|
| Tokenization | ~10ms | O(n) |
| DistilBERT encoding | ~500ms | O(n²) |
| Mean pooling | ~5ms | O(n) |
| Keyword extraction | ~100ms | O(k·n) |
| Cosine similarity | ~100ms | O(m) where m=1,193 |
| Scoring | ~5ms | O(50) |
| Modifier detection | ~10ms | O(n) |
| **Total** | **~730ms** | **GPU-accelerated** |

---

## How to Use This Baseline

### 1. Run Interactive Mode
```bash
cd affective_component/affective_baseline
python main.py
```

### 2. Integrate into Code
```python
from Core.profile_builder import build_profile
from transformers import AutoTokenizer, AutoModel
import pandas as pd
import ast

# Load model
tokenizer = AutoTokenizer.from_pretrained("joeddav/distilbert-base-uncased-go-emotions-student")
model = AutoModel.from_pretrained("joeddav/distilbert-base-uncased-go-emotions-student")

# Load lexicon
df = pd.read_csv("Vocabularies/goemotion_vocabulary.csv")
df = df.dropna()
df['embedding'] = [ast.literal_eval(i) for i in df['embedding'].values.tolist()]

# Detect emotions
result = build_profile(
    sentence="I'm nervous about tomorrow",
    window_size=1,
    df=df,
    tokenizer=tokenizer,
    model=model,
    keyword_extraction=True,
    modifier_detection=True
)

emotion_scores = result[0]  # {fear: 0.45, anticipation: 0.30, ...}
keywords = result[1]  # ['nervous', 'tomorrow']
```

---

## Team Onboarding Checklist

- [ ] Read this architecture guide
- [ ] Review file structure diagram
- [ ] Understand data flow (orchestrator → pipeline → output)
- [ ] Run baseline with test inputs (`01_emotion_test_inputs.md`)
- [ ] Trace code execution for one example sentence
- [ ] Read improvements roadmap (`03_improvements_roadmap.md`)
