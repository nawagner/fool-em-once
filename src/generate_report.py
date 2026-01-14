import json
from datetime import datetime
from pathlib import Path

from jinja2 import Template

BASE_DIR = Path(__file__).parent.parent

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
    with open(BASE_DIR / "data" / "results" / "summary.json") as f:
        data = json.load(f)

    template = Template(REPORT_TEMPLATE)
    html = template.render(
        data=data,
        data_json=json.dumps(data),
        generated_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    output_path = BASE_DIR / "output" / "report.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)

    print(f"Report generated: {output_path}")


if __name__ == "__main__":
    generate_report()
