# Emotion Test Inputs - 14 Plutchik Emotions

## Purpose
Test sentences for each of the 14 Plutchik emotions used in the PRIMA Affective Component baseline. All inputs avoid direct emotion keywords to test contextual understanding.

---

## Test Inputs by Emotion

### 1. Anticipation
```
The concert is in two days.
Results come out tomorrow morning.
Only 3 more days until vacation.
The package should arrive any minute now.
My interview is scheduled for Monday.
```

### 2. Anger
```
This is the third time they've canceled on me.
I've been on hold for 45 minutes.
They promoted someone who started last month.
My flight got delayed for the fourth time.
Someone ate my lunch from the fridge again.
```

### 3. Fear
```
I have to give a presentation to 500 people tomorrow.
The doctor wants to run more tests.
I heard strange noises downstairs at 3am.
My savings account is almost empty.
The brakes aren't working properly.
```

### 4. Sadness
```
He didn't show up to my birthday party.
I failed the exam for the third time.
My dog passed away last night.
She said she needs space.
I didn't get the job offer.
```

### 5. Trust
```
She's been my best friend for 20 years.
I can always count on him.
They've never let me down.
My team has my back no matter what.
They stuck with me during the tough times.
```

### 6. Serenity (senerity)
```
Things didn't work out, but that's okay.
I've learned to let go.
I'm at peace with my decision.
Everything happens for a reason.
I'm content with where I am right now.
```

### 7. Joy (joy_ecstasy)
```
I just got accepted into my dream university!
We're having a baby!
My daughter took her first steps today.
I finally finished my thesis!
They said yes to my proposal!
```

### 8. Admiration (admire)
```
She's the most talented person I've ever met.
I want to be like her when I grow up.
His dedication to the project is incredible.
She overcame so many obstacles to get here.
I look up to him so much.
```

### 9. Acceptance
```
Sometimes life takes unexpected turns.
It is what it is.
I've made peace with the situation.
There's no point fighting it anymore.
I've come to terms with what happened.
```

### 10. Surprise (amazement_surprise)
```
I just found $100 in my old jacket.
My ex texted me after 5 years.
I won the raffle!
There's a package at my door I didn't order.
I got a promotion I didn't apply for.
```

### 11. Distraction
```
I can't stop thinking about what happened.
My mind keeps wandering during meetings.
I've been staring at this screen for an hour.
I keep replaying that conversation in my head.
I can't focus on anything today.
```

### 12. Boredom
```
This meeting could have been an email.
I've watched everything on Netflix already.
There's nothing to do in this town.
Another day, same routine.
I'm counting the hours until this is over.
```

### 13. Disgust (disgust_loathing)
```
There's mold growing in the fridge.
He hasn't showered in a week.
I found a hair in my soup.
The bathroom hasn't been cleaned in months.
There are cockroaches in the kitchen.
```

### 14. Interest/Vigilance (interest_vigilance)
```
I wonder what will happen next.
This is getting more interesting.
I need to pay close attention to this.
Something doesn't add up here.
I should keep an eye on the situation.
```

---

## Usage Instructions

### Running the Baseline
```bash
cd affective_component/affective_baseline
python main.py
```

### Testing Process
1. Copy a test sentence from above
2. Paste into the terminal when prompted
3. Review the emotion scores and keywords
4. Compare with expected emotion category

### Expected Behavior
- **Should detect well**: Strong emotional events, direct associations
- **May struggle with**: Contextual implications, cultural nuances, implicit emotions

---

## Current Baseline Specs
- **Model**: DistilBERT fine-tuned on GoEmotions
- **Lexicon**: goemotion_vocabulary.csv (1,193 terms, 14 emotions)
- **Processing time**: ~730ms per sentence
- **Architecture**: Full AWARE 2/8/14 (supports 2, 8, or 14 emotion granularity)
