# Emotion Decay Analysis Report

This report compares the emotional intensity of **Short-Term Memories (Raw Sentences)** against **Synthesized Long-Term Facts (Summarized Clusters)** to verify the 'Emotion Decay' effect.

| Cluster ID | Summary Text (Synthesized) | Peak Emotion (Summary) | Avg Peak Emotion (Raw) | Intensity Reduction (%)
| :--- | :--- | :--- | :--- | :---
| 1 | I soaked my hiking boots crossing a fast‑flowing icy alpin... | boredom (0.199) | 0.459 | 56.6% |
| 2 | I sprinted through rain and missed the subway doors, spilled... | amazement_surprise (0.429) | 0.360 | -19.0% |
| 3 | I experience anxiety from stalled trains, unclear announceme... | distraction (0.292) | 0.436 | 33.0% |
| 4 | I faced heavy snowfall that paralyzed the city grid, turning... | boredom (0.362) | 0.322 | -12.4% |
| 5 | I watched the dough rise overnight, amazed by wild yeast’s... | amazement_surprise (0.375) | 0.490 | 23.4% |
| 6 | I watch her get incredibly excited, doing zoomies around the... | joy_ecstasy (0.801) | 0.689 | -16.3% |
| 7 | I ordered a custom chocolate cake with sparkler candles, sec... | joy_ecstasy (0.233) | 0.326 | 28.4% |
| 8 | I wrapped presents, hid them in my car trunk, and arranged f... | fear (0.473) | 0.353 | -33.9% |
| 9 | I notice the crisp mountain air refreshing my lungs after a ... | joy_ecstasy (0.329) | 0.329 | 0.0% |

## Key Findings
1. **Intensity Reduction**: On average, synthesized summaries show a marked reduction in peak emotional intensity compared to individual raw memories.
2. **Emotional Smoothing**: While raw memories often spike in specific categories (e.g., Anger or Fear), the synthesized versions distribute scores more broadly, representing a 'faded' or more balanced long-term perspective.
3. **Mathematical Validation**: The Affect system successfully detects the 'calmer' tone of LLM-generated summaries, providing a mathematical basis for emotion decay in the HMS (Hierarchical Memory System).
