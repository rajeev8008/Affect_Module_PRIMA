# Affective Component

This folder contains the emotion detection module for PRIMA, organized into baseline and improved versions.

## Structure

```
affective_component/
├── affective_baseline/     # Frozen baseline for comparison
└── affective_improved/     # Optimized version with improvements
```

## Folders

### `affective_baseline/`
- **Purpose**: Frozen reference implementation
- **Status**: DO NOT MODIFY
- **Use**: Baseline benchmarks and dissertation comparisons
- **Performance**: ~730ms/sentence (measured)
- **Benchmark Status**: **COMPLETED** - Validated with ISEAR, GoEmotions, Senti4SD, and PhraseBank datasets

### `affective_improved/`
- **Purpose**: Optimized version with performance/accuracy improvements
- **Status**: Active development
- **Use**: PRIMA integration
- **Target Performance**: ~30ms/sentence (20x faster goal)
- **Target Accuracy**: F1=0.74 (projected after improvements)
- **Benchmark Status**: **PENDING** - awaiting implementation and testing

## Usage

### Running Baseline
```bash
cd affective_baseline
python main.py
```

### Running Improved (after implementation)
```bash
cd affective_improved
python main.py
```

## Development Workflow

1. **Never modify** `affective_baseline/` - it's frozen for comparison
2. **Develop improvements** in `affective_improved/`
3. **Benchmark** both versions using `evaluation/` scripts
4. **Document** improvements for dissertation

---

**Created**: 2026-02-03  
**Last Updated**: 2026-02-03
