import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


class AnalyzeResultsParsingTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_csv(self, path: Path, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    def _write_manifest(self, essays):
        manifest_path = (
            self.base_dir
            / "data"
            / "essays"
            / "original"
            / "manifest_all.json"
        )
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, "w") as handle:
            json.dump(essays, handle)

    def test_analyze_parses_yes_no_values(self):
        essays = [
            {
                "id": "gemini-3-flash_hist-01",
                "model": "gemini-3-flash",
                "category": "historical",
            },
            {
                "id": "gpt-5.2_lit-01",
                "model": "gpt-5.2",
                "category": "literature",
            },
            {
                "id": "gemini-3-flash_sci-01",
                "model": "gemini-3-flash",
                "category": "scientific",
            },
            {
                "id": "gpt-5.2_pers-01",
                "model": "gpt-5.2",
                "category": "personal",
            },
        ]
        self._write_manifest(essays)

        baseline_rows = []
        post_rows = []
        detector_values = {
            "writehuman": ["yes", "yes", "yes", "no"],
            "pangram": ["yes", "no", "no", "yes"],
            "gptzero": ["yes", "yes", "yes", "yes"],
        }
        for detector, values in detector_values.items():
            for essay, is_ai in zip(essays, values):
                baseline_rows.append(
                    {
                        "essay_id": essay["id"],
                        "detector": detector,
                        "is_ai_detected": is_ai,
                        "confidence": 50,
                        "notes": "",
                    }
                )
                post_rows.append(
                    {
                        "essay_id": essay["id"],
                        "detector": detector,
                        "is_ai_detected": "no",
                        "confidence": 10,
                        "notes": "",
                    }
                )

        self._write_csv(
            self.base_dir / "data" / "results" / "baseline" / "results.csv",
            baseline_rows,
        )
        self._write_csv(
            self.base_dir
            / "data"
            / "results"
            / "post_humanization"
            / "results.csv",
            post_rows,
        )

        repo_root = Path(__file__).resolve().parents[1]
        sys.path.insert(0, str(repo_root / "src"))
        import analyze_results  # noqa: E402

        analyze_results.BASE_DIR = self.base_dir
        summary = analyze_results.analyze()

        self.assertAlmostEqual(
            summary["by_detector"]["writehuman"]["baseline_detection_rate"], 75.0
        )
        self.assertAlmostEqual(
            summary["by_detector"]["pangram"]["baseline_detection_rate"], 50.0
        )
        self.assertAlmostEqual(
            summary["by_detector"]["gptzero"]["baseline_detection_rate"], 100.0
        )
        self.assertAlmostEqual(summary["overall"]["baseline_detection_rate"], 75.0)
        self.assertAlmostEqual(summary["overall"]["post_detection_rate"], 0.0)
        self.assertAlmostEqual(summary["overall"]["avg_bypass_rate"], 75.0)


if __name__ == "__main__":
    unittest.main()
