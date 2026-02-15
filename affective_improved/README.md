# Affective Component - Improved

Optimized version with performance and accuracy improvements over baseline.

## Planned Improvements

### Phase 1: Performance (High Priority)
- [ ] FAISS similarity search (20-50x faster)
- [ ] Batch processing (10-20x throughput)
- [ ] Mixed precision inference (2x faster, 50% less VRAM)

### Phase 2: Quality (Medium Priority)
- [ ] Attention-based keyword extraction
- [ ] Vector database for lexicon (ChromaDB)
- [ ] LRU caching for repeated queries

### Phase 3: Advanced (Optional)
- [ ] Learned modifier handling (context-aware)
- [ ] RoBERTa-large model upgrade

## Target Metrics
- **Speed**: 0.03s per sentence (20x faster than baseline)
- **Throughput**: 33 sentences/sec
- **F1-Score**: 0.74 (+12% improvement)
- **Memory**: 0.8 GB VRAM (-47% reduction)

## Current Status
- ✅ Copied from baseline
- ⏳ Ready for improvements

---

**Created**: 2026-02-03  
**Status**: Active development
