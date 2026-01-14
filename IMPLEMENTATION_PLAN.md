# Implementation Plan: AI Text Humanizer Effectiveness Study

## Project Structure

```
san-jose/
├── SOURCE_PROMPT.md              # Original requirements
├── IMPLEMENTATION_PLAN.md        # This file
├── .env.local                    # OpenRouter API key
├── requirements.txt              # Python dependencies
├── src/
│   ├── config.py                 # Topics and model configurations
│   ├── generate_essays.py        # OpenRouter essay generation
│   ├── analyze_results.py        # Data analysis
│   └── generate_report.py        # HTML report generation
├── data/
│   ├── essays/
│   │   ├── original/             # Raw AI-generated essays (JSON + individual .txt)
│   │   └── humanized/            # Post-humanization essays (manually added)
│   └── results/
│       ├── baseline/             # Manual detection results (CSV)
│       ├── post_humanization/    # Post-humanization detection results (CSV)
│       └── summary.json          # Aggregated analysis
└── output/
    └── report.html               # Final visualization report
```

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          AUTOMATED                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  1. Generate Essays (Python + OpenRouter API)                           │
│     → Outputs: data/essays/original/*.txt                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          MANUAL                                          │
├─────────────────────────────────────────────────────────────────────────┤
│  2. Baseline Detection                                                   │
│     → Copy/paste each essay into 3 detectors                            │
│     → Record results in: data/results/baseline/results.csv              │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          MANUAL                                          │
├─────────────────────────────────────────────────────────────────────────┤
│  3. Humanization                                                         │
│     → Copy/paste each essay into WriteHuman.ai                          │
│     → Save outputs to: data/essays/humanized/*.txt                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          MANUAL                                          │
├─────────────────────────────────────────────────────────────────────────┤
│  4. Post-Humanization Detection                                          │
│     → Copy/paste each humanized essay into 3 detectors                  │
│     → Record results in: data/results/post_humanization/results.csv     │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          AUTOMATED                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  5. Analysis & Report Generation (Python)                                │
│     → Outputs: output/report.html                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Project Setup

### 1.1 Dependencies

```txt
# requirements.txt
openai>=1.0.0
python-dotenv>=1.0.0
pandas>=2.0.0
jinja2>=3.0.0
```

### 1.2 Install

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Phase 2: Configuration

```python
# src/config.py

from dataclasses import dataclass
from enum import Enum

class Category(Enum):
    HISTORICAL = "historical"
    LITERATURE = "literature"
    SCIENTIFIC = "scientific"
    PERSONAL = "personal"

@dataclass
class Topic:
    id: str
    category: Category
    title: str
    prompt: str

# Model IDs for OpenRouter
MODELS = {
    "gemini-3-flash": "google/gemini-3-flash-preview",
    "gpt-5.2": "openai/gpt-5.2",
}

TOPICS = [
    # Historical (5)
    Topic("hist-01", Category.HISTORICAL, "Richest Person in History",
          "Write a 500-word high school essay on: Who is really the richest person in history?"),
    Topic("hist-02", Category.HISTORICAL, "Korean Comfort Women",
          "Write a 500-word high school essay on: The story of Korean comfort women and their impact on modern day Japanese-Korean relations"),
    Topic("hist-03", Category.HISTORICAL, "American Industrial Espionage",
          "Write a 500-word high school essay on: American industrial espionage in the late 18th and early 19th centuries"),
    Topic("hist-04", Category.HISTORICAL, "Rosa Parks After Montgomery",
          "Write a 500-word high school essay on: Rosa Parks' contribution to Civil Rights after the Montgomery bus boycott"),
    Topic("hist-05", Category.HISTORICAL, "Cane Toads in Australia",
          "Write a 500-word high school essay on: The lessons learned from introducing cane toads in Australia"),

    # Literature (5)
    Topic("lit-01", Category.LITERATURE, "Frankenstein and AI",
          "Write a 500-word high school literary analysis on: Mary Shelley's Frankenstein's relevance to modern debates on artificial intelligence"),
    Topic("lit-02", Category.LITERATURE, "1984 vs Brave New World",
          "Write a 500-word high school literary analysis on: Between 1984 and Brave New World, which dystopia is more likely to become true and why?"),
    Topic("lit-03", Category.LITERATURE, "Whitman and Civil War",
          "Write a 500-word high school literary analysis on: How Walt Whitman's experience in the Civil War influenced his poetry"),
    Topic("lit-04", Category.LITERATURE, "Rumi as Sufi Mystic",
          "Write a 500-word high school literary analysis on: The poet Rumi's role as a Sufi mystic and how his work (like the Masnavi) reflects Islamic mystical tradition"),
    Topic("lit-05", Category.LITERATURE, "Machiavelli's Prince",
          "Write a 500-word high school literary analysis on: Is Machiavelli's The Prince a genuine guide for tyrants or a satirical critique?"),

    # Scientific (5)
    Topic("sci-01", Category.SCIENTIFIC, "Geoengineering Water Cycle",
          "Write a 500-word high school science essay on: Methods of geoengineering the water cycle and their potential drawbacks"),
    Topic("sci-02", Category.SCIENTIFIC, "Earthquake Detectors",
          "Write a 500-word high school science essay on: How do earthquake detectors work?"),
    Topic("sci-03", Category.SCIENTIFIC, "Eutectics in Metals",
          "Write a 500-word high school science essay on: What are eutectics and why do they matter for metals engineering?"),
    Topic("sci-04", Category.SCIENTIFIC, "Fermi Paradox",
          "Write a 500-word high school science essay on: What is the Fermi paradox and what are some likely explanations?"),
    Topic("sci-05", Category.SCIENTIFIC, "Continental Drift Evidence",
          "Write a 500-word high school science essay on: What evidence do we have that Earth's continents were once contiguous?"),

    # Personal (5)
    Topic("pers-01", Category.PERSONAL, "Mom's Cooking Appreciation",
          "Write a 500-word personal essay from the perspective of a half Chinese and half German-American teenager who was at first ashamed of their Malaysian immigrant mom's cooking but grew to appreciate it and their culture."),
    Topic("pers-02", Category.PERSONAL, "Perfect Chill Day",
          "Write a 500-word personal essay describing being a chill person whose perfect day is making a cup of tea, reading a book, getting lunch with friends, playing co-op video games, and watching TV beside their cat."),
    Topic("pers-03", Category.PERSONAL, "Social Media Relationship",
          "Write a 500-word personal essay about having a complicated relationship with social media - how it connects to friends and family but also saps attention span and causes jealousy of others' superficial portrayals."),
    Topic("pers-04", Category.PERSONAL, "Interview Embarrassment",
          "Write a 500-word personal essay about how completely embarrassing oneself at a high school prep entrance interview showed they were genuine and able to grow."),
    Topic("pers-05", Category.PERSONAL, "Bali Healing Journey",
          "Write a 500-word personal essay about how a trip to Bali after a divorce helped heal emotional trauma and reconnect with an authentic self."),
]

def get_topics_by_category(category: Category) -> list[Topic]:
    return [t for t in TOPICS if t.category == category]
```

---

## Phase 3: Essay Generation (Automated)

```python
# src/generate_essays.py

import os
import json
import time
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from config import MODELS, TOPICS, Topic, Category, get_topics_by_category

load_dotenv(".env.local")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

OUTPUT_DIR = Path("data/essays/original")


def generate_essay(topic: Topic, model_key: str) -> dict:
    """Generate a single essay using OpenRouter."""
    model_id = MODELS[model_key]

    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "system",
                "content": "You are a high school student writing an essay for class. Write naturally and authentically as a student would. Do not use overly sophisticated vocabulary or perfect structure."
            },
            {
                "role": "user",
                "content": topic.prompt
            }
        ],
        max_tokens=800,
        temperature=0.7,
    )

    content = response.choices[0].message.content
    word_count = len(content.split())

    return {
        "id": f"{model_key}_{topic.id}",
        "topic_id": topic.id,
        "topic_title": topic.title,
        "category": topic.category.value,
        "model": model_key,
        "content": content,
        "word_count": word_count,
    }


def generate_essays_for_category(category: Category, models: list[str] = None):
    """Generate essays for a single category (for pilot testing)."""
    if models is None:
        models = list(MODELS.keys())

    topics = get_topics_by_category(category)
    essays = []

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for model_key in models:
        for topic in topics:
            essay_id = f"{model_key}_{topic.id}"
            print(f"Generating: {essay_id} - {topic.title}")

            essay = generate_essay(topic, model_key)
            essays.append(essay)

            # Save individual text file for easy copy/paste
            txt_path = OUTPUT_DIR / f"{essay_id}.txt"
            txt_path.write_text(essay["content"])

            # Rate limiting
            time.sleep(1)

    # Save manifest
    manifest_path = OUTPUT_DIR / f"manifest_{category.value}.json"
    with open(manifest_path, "w") as f:
        json.dump(essays, f, indent=2)

    print(f"\nGenerated {len(essays)} essays for {category.value}")
    print(f"Individual files saved to: {OUTPUT_DIR}/")
    print(f"Manifest saved to: {manifest_path}")

    return essays


def generate_all_essays():
    """Generate all 40 essays."""
    all_essays = []

    for category in Category:
        essays = generate_essays_for_category(category)
        all_essays.extend(essays)
        time.sleep(2)  # Pause between categories

    # Save complete manifest
    manifest_path = OUTPUT_DIR / "manifest_all.json"
    with open(manifest_path, "w") as f:
        json.dump(all_essays, f, indent=2)

    print(f"\nTotal essays generated: {len(all_essays)}")
    return all_essays


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Pilot mode: generate for specific category
        category_name = sys.argv[1].upper()
        category = Category[category_name]
        generate_essays_for_category(category)
    else:
        # Full generation
        generate_all_essays()
```

**Usage:**
```bash
# Pilot test with one category
python src/generate_essays.py historical

# Full generation (all 40 essays)
python src/generate_essays.py
```

---

## Phase 4: Manual Detection Workflow

### 4.1 CSV Template for Recording Results

Create `data/results/baseline/results.csv`:

```csv
essay_id,detector,is_ai_detected,confidence,notes
gemini-3-flash_hist-01,writehuman,true,92,
gemini-3-flash_hist-01,pangram,true,88,
gemini-3-flash_hist-01,gptzero,true,95,
```

### 4.2 Detection Checklist

For each essay in `data/essays/original/`:

1. **WriteHuman AI Detector** (https://writehuman.ai/ai-detector)
   - Paste essay text
   - Record: detected (yes/no), confidence %

2. **Pangram** (https://www.pangram.com/)
   - Paste essay text
   - Record: detected (yes/no), confidence %

3. **GPTZero** (https://gptzero.me/)
   - Paste essay text
   - Record: detected (yes/no), confidence %

### 4.3 Tracking Progress

```
Detection Progress (Baseline):
[ ] gemini-3-flash_hist-01: WH☐ PG☐ GZ☐
[ ] gemini-3-flash_hist-02: WH☐ PG☐ GZ☐
...
[ ] gpt-5.2_hist-05: WH☐ PG☐ GZ☐
```

---

## Phase 5: Manual Humanization Workflow

### 5.1 Process

For each essay in `data/essays/original/`:

1. Go to https://writehuman.ai/
2. Paste the essay text
3. Click "Humanize"
4. Copy the output
5. Save to `data/essays/humanized/{essay_id}.txt`

### 5.2 Directory Structure After Humanization

```
data/essays/humanized/
├── gemini-3-flash_hist-01.txt
├── gemini-3-flash_hist-02.txt
├── ...
└── gpt-5.2_pers-05.txt
```

---

## Phase 6: Post-Humanization Detection (Manual)

Same as Phase 4, but:
- Use essays from `data/essays/humanized/`
- Save results to `data/results/post_humanization/results.csv`

---

## Phase 7: Analysis (Automated)

```python
# src/analyze_results.py

import json
import pandas as pd
from pathlib import Path

def load_results():
    """Load baseline and post-humanization results."""
    baseline = pd.read_csv("data/results/baseline/results.csv")
    post = pd.read_csv("data/results/post_humanization/results.csv")

    # Load essay manifest for metadata
    with open("data/essays/original/manifest_all.json") as f:
        essays = json.load(f)
    essays_df = pd.DataFrame(essays)

    return baseline, post, essays_df


def analyze():
    """Generate summary statistics."""
    baseline, post, essays = load_results()

    # Merge with essay metadata
    baseline = baseline.merge(
        essays[["id", "model", "category"]],
        left_on="essay_id",
        right_on="id"
    )
    post = post.merge(
        essays[["id", "model", "category"]],
        left_on="essay_id",
        right_on="id"
    )

    summary = {
        "total_essays": len(essays),
        "total_detections": len(baseline) + len(post),

        "by_detector": {},
        "by_model": {},
        "by_category": {},
    }

    # By detector
    for detector in ["writehuman", "pangram", "gptzero"]:
        b = baseline[baseline["detector"] == detector]
        p = post[post["detector"] == detector]

        baseline_rate = b["is_ai_detected"].mean() * 100
        post_rate = p["is_ai_detected"].mean() * 100

        summary["by_detector"][detector] = {
            "baseline_detection_rate": round(baseline_rate, 1),
            "post_detection_rate": round(post_rate, 1),
            "bypass_rate": round(baseline_rate - post_rate, 1),
        }

    # By model
    for model in ["gemini-3-flash", "gpt-5.2"]:
        b = baseline[baseline["model"] == model]
        p = post[post["model"] == model]

        summary["by_model"][model] = {
            "baseline_detection_rate": round(b["is_ai_detected"].mean() * 100, 1),
            "post_detection_rate": round(p["is_ai_detected"].mean() * 100, 1),
        }

    # By category
    for category in ["historical", "literature", "scientific", "personal"]:
        b = baseline[baseline["category"] == category]
        p = post[post["category"] == category]

        summary["by_category"][category] = {
            "baseline_detection_rate": round(b["is_ai_detected"].mean() * 100, 1),
            "post_detection_rate": round(p["is_ai_detected"].mean() * 100, 1),
        }

    # Overall
    summary["overall"] = {
        "baseline_detection_rate": round(baseline["is_ai_detected"].mean() * 100, 1),
        "post_detection_rate": round(post["is_ai_detected"].mean() * 100, 1),
        "avg_bypass_rate": round(
            (baseline["is_ai_detected"].mean() - post["is_ai_detected"].mean()) * 100, 1
        ),
    }

    # Save
    with open("data/results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    analyze()
```

---

## Phase 8: Report Generation (Automated)

```python
# src/generate_report.py

import json
from pathlib import Path
from jinja2 import Template

REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Text Humanizer Effectiveness Study</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      --bg-primary: #0f172a;
      --bg-secondary: #1e293b;
      --bg-tertiary: #334155;
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --accent: #3b82f6;
      --success: #22c55e;
      --warning: #f59e0b;
      --danger: #ef4444;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg-primary);
      color: var(--text-primary);
      line-height: 1.6;
      padding: 2rem;
    }
    .container { max-width: 1400px; margin: 0 auto; }
    header { text-align: center; margin-bottom: 3rem; padding-bottom: 2rem; border-bottom: 1px solid var(--bg-tertiary); }
    h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
    h2 { font-size: 1.5rem; margin: 2rem 0 1rem; color: var(--text-primary); }
    .subtitle { color: var(--text-secondary); font-size: 1.1rem; }
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 3rem; }
    .stat-card { background: var(--bg-secondary); border-radius: 12px; padding: 1.5rem; text-align: center; }
    .stat-value { font-size: 2.5rem; font-weight: 700; }
    .stat-value.accent { color: var(--accent); }
    .stat-value.success { color: var(--success); }
    .stat-value.danger { color: var(--danger); }
    .stat-label { color: var(--text-secondary); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.5rem; }
    .charts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 2rem; margin-bottom: 3rem; }
    .chart-container { background: var(--bg-secondary); border-radius: 12px; padding: 1.5rem; }
    .chart-title { font-size: 1.1rem; margin-bottom: 1rem; }
    .methodology { background: var(--bg-secondary); border-radius: 12px; padding: 2rem; margin-top: 2rem; }
    .methodology h3 { margin-bottom: 1rem; }
    .methodology ul { margin-left: 1.5rem; color: var(--text-secondary); }
    .methodology li { margin-bottom: 0.5rem; }
    .footer { text-align: center; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--bg-tertiary); color: var(--text-secondary); font-size: 0.9rem; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>AI Text Humanizer Effectiveness Study</h1>
      <p class="subtitle">Evaluating WriteHuman.ai's ability to bypass AI detection tools</p>
    </header>

    <section class="stats-grid">
      <div class="stat-card">
        <div class="stat-value accent">{{ data.total_essays }}</div>
        <div class="stat-label">Total Essays</div>
      </div>
      <div class="stat-card">
        <div class="stat-value danger">{{ data.overall.baseline_detection_rate }}%</div>
        <div class="stat-label">Baseline Detection Rate</div>
      </div>
      <div class="stat-card">
        <div class="stat-value success">{{ data.overall.post_detection_rate }}%</div>
        <div class="stat-label">Post-Humanization Detection</div>
      </div>
      <div class="stat-card">
        <div class="stat-value success">{{ data.overall.avg_bypass_rate }}%</div>
        <div class="stat-label">Average Bypass Rate</div>
      </div>
    </section>

    <h2>Detection by Tool</h2>
    <section class="charts-grid">
      <div class="chart-container">
        <h3 class="chart-title">Detection Rate Comparison</h3>
        <canvas id="detectorChart"></canvas>
      </div>
      <div class="chart-container">
        <h3 class="chart-title">Bypass Rate by Detector</h3>
        <canvas id="bypassChart"></canvas>
      </div>
    </section>

    <h2>Detection by Model</h2>
    <section class="charts-grid">
      <div class="chart-container">
        <h3 class="chart-title">Model Comparison</h3>
        <canvas id="modelChart"></canvas>
      </div>
      <div class="chart-container">
        <h3 class="chart-title">Category Comparison</h3>
        <canvas id="categoryChart"></canvas>
      </div>
    </section>

    <section class="methodology">
      <h3>Methodology</h3>
      <ul>
        <li><strong>Essay Generation:</strong> 40 essays (500 words each) generated via OpenRouter using Gemini-3-flash and GPT-5.2</li>
        <li><strong>Topics:</strong> 20 unique topics across 4 categories (Historical, Literature, Scientific, Personal)</li>
        <li><strong>Detection Tools:</strong> WriteHuman AI Detector, Pangram, GPTZero</li>
        <li><strong>Humanization:</strong> All essays processed through WriteHuman.ai</li>
        <li><strong>Metrics:</strong> Binary detection (AI/Human) with confidence scores</li>
      </ul>
    </section>

    <footer>
      <p>Generated on {{ generated_date }}</p>
    </footer>
  </div>

  <script>
    const data = {{ data_json | safe }};

    Chart.defaults.color = '#94a3b8';
    Chart.defaults.borderColor = '#334155';

    // Detector comparison
    new Chart(document.getElementById('detectorChart'), {
      type: 'bar',
      data: {
        labels: ['WriteHuman', 'Pangram', 'GPTZero'],
        datasets: [
          {
            label: 'Baseline',
            data: [
              data.by_detector.writehuman.baseline_detection_rate,
              data.by_detector.pangram.baseline_detection_rate,
              data.by_detector.gptzero.baseline_detection_rate
            ],
            backgroundColor: 'rgba(239, 68, 68, 0.8)',
          },
          {
            label: 'Post-Humanization',
            data: [
              data.by_detector.writehuman.post_detection_rate,
              data.by_detector.pangram.post_detection_rate,
              data.by_detector.gptzero.post_detection_rate
            ],
            backgroundColor: 'rgba(34, 197, 94, 0.8)',
          }
        ]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true, max: 100, title: { display: true, text: 'Detection Rate (%)' } } }
      }
    });

    // Bypass rate
    new Chart(document.getElementById('bypassChart'), {
      type: 'bar',
      data: {
        labels: ['WriteHuman', 'Pangram', 'GPTZero'],
        datasets: [{
          label: 'Bypass Rate',
          data: [
            data.by_detector.writehuman.bypass_rate,
            data.by_detector.pangram.bypass_rate,
            data.by_detector.gptzero.bypass_rate
          ],
          backgroundColor: 'rgba(59, 130, 246, 0.8)',
        }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true, title: { display: true, text: 'Bypass Rate (%)' } } }
      }
    });

    // Model comparison
    new Chart(document.getElementById('modelChart'), {
      type: 'bar',
      data: {
        labels: ['Gemini-3-flash', 'GPT-5.2'],
        datasets: [
          {
            label: 'Baseline',
            data: [
              data.by_model['gemini-3-flash'].baseline_detection_rate,
              data.by_model['gpt-5.2'].baseline_detection_rate
            ],
            backgroundColor: 'rgba(239, 68, 68, 0.8)',
          },
          {
            label: 'Post-Humanization',
            data: [
              data.by_model['gemini-3-flash'].post_detection_rate,
              data.by_model['gpt-5.2'].post_detection_rate
            ],
            backgroundColor: 'rgba(34, 197, 94, 0.8)',
          }
        ]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true, max: 100, title: { display: true, text: 'Detection Rate (%)' } } }
      }
    });

    // Category comparison
    new Chart(document.getElementById('categoryChart'), {
      type: 'bar',
      data: {
        labels: ['Historical', 'Literature', 'Scientific', 'Personal'],
        datasets: [
          {
            label: 'Baseline',
            data: [
              data.by_category.historical.baseline_detection_rate,
              data.by_category.literature.baseline_detection_rate,
              data.by_category.scientific.baseline_detection_rate,
              data.by_category.personal.baseline_detection_rate
            ],
            backgroundColor: 'rgba(239, 68, 68, 0.8)',
          },
          {
            label: 'Post-Humanization',
            data: [
              data.by_category.historical.post_detection_rate,
              data.by_category.literature.post_detection_rate,
              data.by_category.scientific.post_detection_rate,
              data.by_category.personal.post_detection_rate
            ],
            backgroundColor: 'rgba(34, 197, 94, 0.8)',
          }
        ]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true, max: 100, title: { display: true, text: 'Detection Rate (%)' } } }
      }
    });
  </script>
</body>
</html>
"""


def generate_report():
    """Generate the HTML report from summary data."""
    from datetime import datetime

    with open("data/results/summary.json") as f:
        data = json.load(f)

    template = Template(REPORT_TEMPLATE)
    html = template.render(
        data=data,
        data_json=json.dumps(data),
        generated_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    output_path = Path("output/report.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)

    print(f"Report generated: {output_path}")


if __name__ == "__main__":
    generate_report()
```

---

## Execution Checklist

### Pilot Test (Historical Category Only)
```bash
# 1. Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Generate essays (10 essays: 5 topics x 2 models)
python src/generate_essays.py historical

# 3. Manual: Run baseline detection on 10 essays x 3 detectors
#    Record in data/results/baseline/results.csv

# 4. Manual: Humanize 10 essays via WriteHuman.ai
#    Save to data/essays/humanized/

# 5. Manual: Run post-humanization detection
#    Record in data/results/post_humanization/results.csv

# 6. Analyze and generate report
python src/analyze_results.py
python src/generate_report.py
```

### Full Study (All 40 Essays)
```bash
python src/generate_essays.py  # Generates all 40
# ... manual detection and humanization ...
python src/analyze_results.py
python src/generate_report.py
```

---

## Time Estimates

| Phase | Automated | Manual | Notes |
|-------|-----------|--------|-------|
| Essay Generation | ~10 min | - | API rate limits |
| Baseline Detection | - | ~2-3 hrs | 40 essays x 3 detectors |
| Humanization | - | ~1-2 hrs | 40 essays |
| Post Detection | - | ~2-3 hrs | 40 essays x 3 detectors |
| Analysis & Report | ~1 min | - | Python scripts |

**Pilot (Historical only):** ~1.5 hrs manual work
**Full Study:** ~6-8 hrs manual work
