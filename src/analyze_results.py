import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent

TRUE_VALUES = ["true", "True", "TRUE", "yes", "Yes", "YES", "ai", "AI", "1"]
FALSE_VALUES = ["false", "False", "FALSE", "no", "No", "NO", "human", "Human", "HUMAN", "0"]


def load_results():
    """Load baseline and post-humanization results."""
    baseline = pd.read_csv(
        BASE_DIR / "data" / "results" / "baseline" / "results.csv",
        true_values=TRUE_VALUES,
        false_values=FALSE_VALUES,
    )
    post = pd.read_csv(
        BASE_DIR / "data" / "results" / "post_humanization" / "results.csv",
        true_values=TRUE_VALUES,
        false_values=FALSE_VALUES,
    )

    # Load essay manifest for metadata
    manifest_path = BASE_DIR / "data" / "essays" / "original" / "manifest_all.json"
    with open(manifest_path) as f:
        essays = json.load(f)
    essays_df = pd.DataFrame(essays)

    return baseline, post, essays_df


def analyze():
    """Generate summary statistics."""
    baseline, post, essays = load_results()

    # Merge with essay metadata
    baseline = baseline.merge(
        essays[["id", "model", "category"]], left_on="essay_id", right_on="id"
    )
    post = post.merge(
        essays[["id", "model", "category"]], left_on="essay_id", right_on="id"
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
    results_dir = BASE_DIR / "data" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    with open(results_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    analyze()
