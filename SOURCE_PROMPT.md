# AI Text Humanizer Effectiveness Study

## Overview

A study to evaluate how well AI text humanizers (specifically WriteHuman.ai) can bypass AI detection tools.

## Study Procedure

1. **Generate synthetic texts** - Create AI-generated essays using two different LLMs
2. **Baseline detection** - Run synthetic texts through AI detectors and record whether they correctly identify them as AI-generated
3. **Humanize texts** - Process all texts through [WriteHuman.ai](https://writehuman.ai/) text humanizer
4. **Post-humanization detection** - Run humanized versions through the same AI detectors and record performance
5. **Summarize findings** - Create an HTML page with visualizations of the results

---

## Synthetic Text Generation

### Specifications
- **Total texts:** 40
- **Word count per text:** 500 words
- **Format:** High school level essays
- **API Access:** OpenRouter

### Models
| Model | Text Count |
|-------|------------|
| Gemini-3-flash | 20 |
| GPT-5.2 | 20 |

Each model will generate essays on all 20 topics (one per topic).

---

## Essay Topics

### Historical Topics (5)
1. Who is really the richest person in history
2. Story of Korean comfort women and their impact on modern day Japanese-Korean relations
3. American industrial espionage in the late 18th and early 19th centuries
4. Rosa Parks' contribution to Civil Rights after the Montgomery bus boycott
5. The lessons learned from introducing cane toads in Australia

### English Literature Analysis (5)
1. Mary Shelley's Frankenstein's relevance to modern debates on artificial intelligence
2. Between 1984 and Brave New World, which dystopia is more likely to become true and why?
3. How Walt Whitman's experience in the Civil War influenced his poetry
4. Explain the poet Rumi's role as a Sufi mystic and how his work (like the Masnavi) reflects Islamic mystical tradition
5. Is Machiavelli's The Prince a genuine guide for tyrants or a satirical critique?

### Scientific Topics (5)
1. Methods of geoengineering the water cycle and their potential drawbacks
2. How do earthquake detectors work?
3. What are eutectics and why do they matter for metals engineering?
4. What is the Fermi paradox and what are some likely explanations?
5. What evidence do we have that Earth's continents were once contiguous?

### Personal Reflections (5)
1. An essay on how I, a half Chinese and half German-American teenager, at first was ashamed of my Malaysian immigrant mom's cooking but grew to appreciate it and my culture.
2. Describing how I am a chill person whose perfect day is making a cup of tea, reading a book, getting lunch with my friends, playing co-op video games, and watching TV beside my cat.
3. My complicated relationship with social media. On one hand it connects me to my friends and family but on the other it saps my attention span and makes me jealous of others' superficial portrayals.
4. How my experience completely embarrassing myself at my high school prep entrance interview showed I was genuine and able to grow.
5. How my trip to Bali after my divorce helped me heal from my emotional trauma and reconnect with my authentic self.

---

## AI Detectors

| Detector | URL |
|----------|-----|
| WriteHuman AI Detector | http://writehuman.ai/ai-detector |
| Pangram | https://www.pangram.com/ |
| GPTZero | https://gptzero.me/ |

---

## Text Humanizer

- **Service:** [WriteHuman.ai](https://writehuman.ai/)

---

## Expected Outputs

### Data Collection
For each of the 40 texts, record:
- Original AI detection results (3 detectors x 40 texts = 120 data points)
- Post-humanization detection results (3 detectors x 40 texts = 120 data points)

### Final Deliverable
An HTML page with visualizations including:
- Detection accuracy before vs. after humanization
- Breakdown by model (Gemini-3-flash vs GPT-5.2)
- Breakdown by topic category (Historical, Literature, Scientific, Personal)
- Breakdown by detector (WriteHuman, Pangram, GPTZero)
