# PRIMA Affective Module — Issues & Improvement Plan

> **Scope**: Full audit of `affective_baseline/` codebase. No changes will be made until you provide the Memory Module and Reflection Module architectures.

---

## 🔴 CRITICAL Issues (Must Fix)

### 1. Negation Handling is Fundamentally Broken (Study 8: 0.245 vs Paper 0.841)
- **File**: [modifier_handling.py](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/Core/modifier_handling.py#L98-L155)
- **Problem**: Negation is only checked inside the **top-1 keyword window** (3 tokens before it). If the negation word (`"not"`) falls outside this tiny window, it's ignored entirely.
- **Why it fails**: For `"The princess was not happy"`, the keyword window is `"happy"`, the 3-token lookback is `"was not happy"` — this *might* work. But for longer sentences or different structures (e.g., `"I have never been afraid"`), the negation falls outside the window.
- **Root cause**: The negation check at line 146 only runs for `i == 0` (the top-1 candidate window). No sentence-level negation awareness exists.
- **Impact**: **60% performance gap** — this is the single biggest issue.

### 2. `map_opposite_emotions()` Flips ALL Emotions, Not Just the Negated One
- **File**: [modifier_handling.py](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/Core/modifier_handling.py#L68-L95)
- **Problem**: When a negation is detected, `map_opposite_emotions()` remaps the **entire** score dictionary (all 14 emotions), not just the one being negated. This distorts the full emotion profile.
- **Impact**: Amplifies negation errors and produces unrealistic score distributions.

### 3. Hardcoded Paths in `eight_and_fourteen.py` and `distributed_gpu_run.py`
- **Files**: [eight_and_fourteen.py:L8-9](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/eight_and_fourteen.py#L8-L9), [distributed_gpu_run.py:L8-9](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/distributed_gpu_run.py#L8-L9)
- **Problem**: Paths like `r"E:\Projects\Emotion_work_Gihan\..."` are hardcoded. These will fail on any machine other than the original author's.
- **Impact**: Code portability broken; `distributed_gpu_run.py` is essentially non-functional.

---

## 🟠 MAJOR Issues (Significant Performance Impact)

### 4. Typo Bug: `senerity` vs `serenity`
- **File**: [eight_and_fourteen.py:L33-36](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/eight_and_fourteen.py#L33-L36)
- **Problem**: The `ft_to_et()` function checks for both `'senerity'` (typo) and `'serenity'` (correct). The vocabulary uses `'serenity'`, so the legacy branch with the typo is dead code, but this indicates the codebase has lingering inconsistencies.

### 5. No Caching of Vocabulary Embeddings
- **File**: [main.py:L14-16](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/main.py#L13-L16)
- **Problem**: `emo_detect_document()` reloads and re-parses the entire vocabulary CSV (`ast.literal_eval` on 1,120 embeddings) **on every call**. The `__main__` block loads it separately again.
- **Impact**: Massive performance overhead for document-level analysis.

### 6. KNN Search is O(n) Brute-Force per Call
- **File**: [get_nearest_neighbors.py:L9-38](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/Core/get_nearest_neighbors.py#L9-L38)
- **Problem**: For every single sentence (and every sliding window), the code iterates over all 1,120 vocabulary entries computing cosine similarity one-by-one in a Python loop. This is extremely slow.
- **Impact**: Each `build_profile()` call runs `cosine_similarity` ~1,120 times × (1 + number_of_windows). With keyword extraction, that's ~7,000+ cosine operations per sentence.

### 7. Proxy Datasets Not Matching Paper's Actual Datasets
- **File**: [dataset_loader.py](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/benchmarks/dataset_loader.py)
- **Issues**:
  - **ISEAR** → uses `dair-ai/emotion` (Twitter data), not the actual ISEAR corpus → Study 1 & 2 results are not directly comparable to the paper
  - **Financial PhraseBank** → uses `zeroshot/twitter-financial-news-sentiment` instead of `financial_phrasebank` → Study 5 domain mismatch
  - **Senti4SD** → falls back to `SetFit/sst2` (movie reviews!) → Study 6 results are SST-2, not actual Stack Overflow tech sentiment
- **Impact**: Benchmark scores are measured against different data distributions than the paper, making direct comparison unreliable.

### 8. Intensity Modifier Only Modifies the Top-1 Emotion Score
- **File**: [modifier_handling.py:L128-143](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/Core/modifier_handling.py#L128-L143)
- **Problem**: When an intensifier/inhibitor is found, only `normalized_score_dict[list(normalized_score_dict.keys())[-1]]` is modified — i.e., only the **last key** (highest-scored emotion after sorting) gets adjusted. Other related emotions are untouched.
- **Impact**: Limits the expressiveness of modifier detection; Study 7 scores plateau.

---

## 🟡 MODERATE Issues (Code Quality / Maintainability)

### 9. Bare `except:` in Bootstrap CI
- **File**: [evaluate_v2.py:L37](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/benchmarks/evaluate_v2.py#L37)
- **Problem**: `except: continue` silently swallows all errors during bootstrap, potentially hiding metric calculation bugs.

### 10. Bug in `evaluate_v2.py` Table Formatting (Study 6)
- **File**: [evaluate_v2.py:L247](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/benchmarks/evaluate_v2.py#L247)
- **Problem**: Line 247 uses `p['f1']['ci']` for the Negative class's F1 column instead of `n['f1']['ci']`. This is a copy-paste bug that reports incorrect CI for negative class F1 in Study 6.

### 11. `optimized_kwd_extractor()` is Dead Code with Debug Prints
- **File**: [profile_builder.py:L57-73](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/Core/profile_builder.py#L57-L73)
- **Problem**: This function is never called (it's commented out at L81). It also has multiple `print()` debug statements and hardcodes `cuda:1`.

### 12. Hardcoded GPU Device `"cuda:1"` in `optimized_kwd_extractor`
- **File**: [profile_builder.py:L60](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/Core/profile_builder.py#L60)
- **Problem**: Even the main `get_mean_pooling_emb` uses a random GPU selection approach that's unnecessary for a single-GPU system.

### 13. No Error Handling for Empty / Very Short Input
- **File**: [profile_builder.py:L76-147](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/Core/profile_builder.py#L76-L147)
- **Problem**: If `sentence` is empty or a single character, the window sliding and embedding logic can produce unexpected results or empty outputs without clear error messages.

### 14. Commented-Out Code Everywhere
- **Files**: `profile_builder.py`, `scoring.py`, `get_nearest_neighbors.py`, `eight_and_fourteen.py`
- **Problem**: Significant amounts of dead commented-out code reduce readability.

### 15. `matplotlib` Imported but Not Used in Production
- **File**: [profile_builder.py:L7](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/Core/profile_builder.py#L7)
- **Problem**: `matplotlib.pyplot` is imported at the top of the core module. It's only used by the `plot_emotional_weight()` function which isn't called by any production code.

### 16. Global Model/Tokenizer Variables in `main.py`
- **File**: [main.py:L13-16](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/main.py#L13-L16)
- **Problem**: `emo_detect_document()` references `tokenizer` and `model` as global variables (defined only in `__main__`). Calling this function from another module will crash with `NameError`.

---

## 🔵 LOW Issues (Minor / Cosmetic)

### 17. Duplicate `check_for_negations()` Function
- **Files**: [profile_builder.py:L167-174](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/Core/profile_builder.py#L167-L174) and [modifier_handling.py:L58-65](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/Core/modifier_handling.py#L58-L65)
- **Problem**: Identical function defined in two files. Only the one in `modifier_handling.py` is used.

### 18. Inconsistent Return Type
- **File**: [profile_builder.py:L147](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/Core/profile_builder.py#L147)
- **Problem**: Returns a `list` `[dict, list]` — should be a named tuple, dataclass, or at least documented properly.

### 19. `map_candidate_to_emotion()` has a Silent Bug
- **File**: [modifier_handling.py:L46](file:///c:/Users/galad/OneDrive/Desktop/Capstone/code/Affect_Module_PRIMA/affective_baseline/Core/modifier_handling.py#L46)
- **Problem**: Line uses `:` instead of `=` → `emo_candi_dict[each_cd[0]]:max(...)` is a no-op expression, not an assignment. The function always returns an empty dict `{}`.

### 20. No Logging in Core Pipeline
- **Files**: All files in `Core/`
- **Problem**: The core pipeline uses `print()` for debugging instead of Python's `logging` module. No log levels, no configurability.

---

## 📋 Improvement Plan (Priority Order)

### Phase 1: Critical Fixes (Immediate — Before Integration)

| # | Action | Target Score Impact | Files |
|---|--------|---------------------|-------|
| 1 | **Rewrite negation detection** — Implement sentence-level negation scope detection (detect negation words anywhere, apply to the correct emotion, not the entire profile) | Study 8: 0.245 → ~0.6+ | `modifier_handling.py` |
| 2 | **Fix `map_opposite_emotions()`** — Only flip the specific negated emotion, not all 14 | Study 8 improvement | `modifier_handling.py` |
| 3 | **Fix copy-paste bug** in evaluate_v2.py (Study 6 negative CI) | Correct reporting | `evaluate_v2.py` |
| 4 | **Fix global variable issue** in `main.py` — Make `emo_detect_document()` accept model/tokenizer as params | API usability | `main.py` |

### Phase 2: Performance Optimization

| # | Action | Impact | Files |
|---|--------|--------|-------|
| 5 | **Vectorize KNN search** — Pre-compute vocabulary embedding matrix, use batch `cosine_similarity` instead of row-by-row loop | ~10-50x speedup | `get_nearest_neighbors.py` |
| 6 | **Cache vocabulary loading** — Load CSV + parse embeddings once, reuse across calls | Eliminate redundant I/O | `main.py`, `profile_builder.py` |
| 7 | **Remove unnecessary imports** (`matplotlib`, dead code) | Faster module loading | `profile_builder.py` |

### Phase 3: Benchmark Accuracy

| # | Action | Impact | Files |
|---|--------|--------|-------|
| 8 | **Replace proxy datasets with originals** — Use actual ISEAR, Financial PhraseBank, and Senti4SD | More accurate paper comparison | `dataset_loader.py` |
| 9 | **Improve modifier detection** — Apply intensity adjustment to all related emotions (not just top-1) | Study 7 improvement | `modifier_handling.py` |

### Phase 4: Code Quality

| # | Action | Impact | Files |
|---|--------|--------|-------|
| 10 | Remove hardcoded paths from `eight_and_fourteen.py` and `distributed_gpu_run.py` | Portability | multiple |
| 11 | Remove duplicate `check_for_negations()` | Clean code | `profile_builder.py` |
| 12 | Replace `print()` with `logging` in Core | Observability | `Core/*.py` |
| 13 | Clean up commented-out code | Readability | all files |
| 14 | Add input validation to `build_profile()` | Robustness | `profile_builder.py` |

### Phase 5: Integration with Memory & Reflection Modules (⏳ Pending Your Input)

| # | Action | Impact | Files |
|---|--------|--------|-------|
| 15 | **Memory Module integration** — Design API contract for emotion history persistence | Context-aware emotion detection | TBD |
| 16 | **Reflection Module integration** — Feed emotion profiles into reflective reasoning | Higher-level emotional understanding | TBD |
| 17 | **Create unified API** — Clean interface for all three modules to communicate | System integration | `main.py` or new `api.py` |

> [!IMPORTANT]
> **Awaiting your Memory Module and Reflection Module architectures** before proceeding with Phase 5. Please share them when ready.

---

## Summary

| Severity | Count | Key Issue |
|----------|-------|-----------|
| 🔴 Critical | 3 | Negation detection broken, hardcoded paths |
| 🟠 Major | 5 | Proxy datasets, no caching, brute-force KNN |
| 🟡 Moderate | 8 | Dead code, bugs in formatting, missing error handling |
| 🔵 Low | 4 | Duplicate functions, inconsistent returns |
| **Total** | **20** | |
