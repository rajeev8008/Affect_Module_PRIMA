# Affective Component Baseline

**⚠️ DO NOT MODIFY THIS FOLDER ⚠️**

This is the frozen baseline implementation of the Emotion AWARE framework.
It serves as the reference for comparison with improved versions.

## Purpose
- Baseline benchmarking
- Dissertation "before" metrics
- Reference implementation

## Usage
```python
from affective_component.affective_baseline.Core.profile_builder import build_profile
# ...
```

## Baseline Metrics
- **Speed**: 0.62s per sentence
- **Throughput**: 1.6 sentences/sec
- **F1-Score**: 0.66 (estimated)
- **Memory**: 1.5 GB VRAM

## Model
- **Architecture**: DistilBERT-base (66M parameters)
- **Fine-tuning**: GoEmotions dataset (58k Reddit comments, 27 emotions)
- **Lexicon**: Plutchik 14-emotion vocabulary (1,120 terms)

## Components
- `Core/profile_builder.py` - Main emotion detection pipeline
- `Core/get_nearest_neighbors.py` - Cosine similarity search
- `Core/modifier_handling.py` - Negation and intensifier detection
- `Core/scoring.py` - Emotion scoring from neighbors
- `Vocabularies/plutchik_with_emobert_vocab.csv` - Emotion lexicon

---

**Created**: 2026-02-03  
**Status**: Frozen for comparison
