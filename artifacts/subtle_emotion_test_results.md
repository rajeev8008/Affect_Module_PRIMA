# Subtle Emotion Test Results

> **Test**: 24 sentences with **no explicit emotion words** (no "happy", "sad", "angry", etc.)
> **Goal**: Test if the model can detect emotions from context/situation alone
> **Model**: DistilBERT + GoEmotions + Plutchik 14-emotion lexicon (1,120 terms)

## Overall Result

| Metric | Value |
|--------|-------|
| **Accuracy (8-emotion)** | **9/24 = 37.5%** |
| Random baseline (8 classes) | 12.5% |
| Performance vs random | **3x better** |

## Per-Emotion Breakdown

| Emotion | Score | Rating | Observation |
|---------|-------|--------|-------------|
| 🟢 Anticipation | **3/3** | Perfect | Model excels at forward-looking context |
| 🟡 Sadness | **2/3** | Good | "goodbye", "passed away" detected; "last train" missed |
| 🟡 Trust | **2/3** | Good | "safe", "asking" detected; "go wrong" confused it |
| 🟠 Joy | **1/3** | Weak | Only "greet" worked; "passed with full marks" → trust |
| 🟠 Anger | **1/3** | Weak | "scratched car" worked; "took credit" → trust (!) |
| 🔴 Fear | **0/3** | Failed | All classified as anticipation instead |
| 🔴 Disgust | **0/3** | Failed | "cockroach in soup" → surprise; "lied" → fear |
| 🔴 Surprise | **0/3** | Failed | "everyone with gifts" → joy; "double salary" → trust |

---

## Detailed Results

### ✅ Anticipation (3/3 — Model's Strongest)
| Sentence | Got | Score | Keyword |
|----------|-----|-------|---------|
| The interview is tomorrow and I have been preparing all week | anticipation | 0.823 | "preparing" |
| We booked the tickets and the flight leaves at dawn | anticipation | 0.706 | "booked" |
| The countdown has started and there are only three days left | anticipation | 0.758 | "countdown" |

### ✅ Sadness (2/3)
| Sentence | Got | Expected | Keyword |
|----------|-----|----------|---------|
| He packed his bags and left without saying goodbye | sadness ✅ | sadness | "goodbye" |
| The house has been empty since grandma passed away | sadness ✅ | sadness | "empty" |
| I watched the last train leave without me on it | disgust ❌ | sadness | "train" |

### ✅ Trust (2/3)
| Sentence | Got | Expected | Keyword |
|----------|-----|----------|---------|
| I told her my biggest secret and she kept it safe | trust ✅ | trust | "safe" |
| He lent me his car keys without asking any questions | trust ✅ | trust | "asking" |
| My mother always knows what to say when things go wrong | sadness ❌ | trust | "things" |

### ⚠️ Joy (1/3)
| Sentence | Got | Expected | Keyword |
|----------|-----|----------|---------|
| My dog ran to greet me when I got home | joy ✅ | joy | "ran" |
| The exam results came out and I passed with full marks | trust ❌ | joy | "exam" |
| She finally said yes after I asked her out | trust ❌ | joy | "yes" |

### ⚠️ Anger (1/3)
| Sentence | Got | Expected | Keyword |
|----------|-----|----------|---------|
| Someone scratched my car in the parking lot again | anger ✅ | anger | "again" |
| My coworker took credit for the project I built alone | trust ❌ | anger | "coworker" |
| The waiter ignored us for thirty minutes straight | disgust ❌ | anger | "ignored" |

### ❌ Fear (0/3 — Model's Weakest)
| Sentence | Got | Expected | Keyword |
|----------|-----|----------|---------|
| The lights went out and I heard footsteps behind me | anticipation ❌ | fear | "lights" |
| The doctor said we need to talk about the test results | anticipation ❌ | fear | "talk" |
| I am giving a presentation to 500 people tomorrow | anticipation ❌ | fear | "presentation" |

> **Key finding**: Fear and anticipation are adjacent on the Plutchik wheel. The model consistently classifies uncertain/tense situations as anticipation rather than fear. This makes sense — without explicit fear words, the contextual signals lean toward "something is coming" (anticipation) rather than "something is threatening" (fear).

### ❌ Disgust (0/3)
| Sentence | Got | Expected | Keyword |
|----------|-----|----------|---------|
| I found a cockroach in my soup at the restaurant | surprise ❌ | disgust | "cockroach" |
| The politician lied about the funds and pocketed the money | fear ❌ | disgust | "lied" |
| The milk in the fridge expired two weeks ago | trust ❌ | disgust | "expired" |

### ❌ Surprise (0/3)
| Sentence | Got | Expected | Keyword |
|----------|-----|----------|---------|
| I opened the door and everyone was standing there with gifts | joy ❌ | surprise | "gifts" |
| The company offered me double the salary I asked for | trust ❌ | surprise | "salary" |
| My ex showed up at the wedding uninvited | anticipation ❌ | surprise | "uninvited" |

---

## Key Insights

1. **The model is a keyword matcher, not a situation understander** — When words like "safe", "goodbye", "countdown" appear, it detects the right emotion. When the emotion comes from context (500 people = scary), it fails.

2. **Fear–Anticipation confusion is systematic** — All 3 fear sentences were classified as anticipation. These are adjacent emotions on the Plutchik wheel, and without explicit threat words, the model defaults to anticipation.

3. **Disgust and Surprise require explicit cues** — The model has no path to infer disgust from "cockroach in soup" or surprise from "everyone standing with gifts" without emotion-bearing words.

4. **Trust is over-predicted** — Appears 5 times as a false positive across joy, anger, and surprise test cases. The lexicon seems to have a trust bias.
