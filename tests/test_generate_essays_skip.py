import tempfile
import unittest
from pathlib import Path


class GenerateEssaysSkipTest(unittest.TestCase):
    def test_generate_essays_for_category_skips_existing_files(self):
        import sys
        from pathlib import Path as _Path

        repo_root = _Path(__file__).resolve().parents[1]
        sys.path.insert(0, str(repo_root / "src"))

        import generate_essays  # noqa: E402
        from config import Category, Topic  # noqa: E402

        temp_dir = tempfile.TemporaryDirectory()
        output_dir = Path(temp_dir.name) / "data" / "essays" / "original"
        output_dir.mkdir(parents=True, exist_ok=True)

        topic = Topic(
            "hist-99",
            Category.HISTORICAL,
            "Test Topic",
            "Write a 500-word essay about tests.",
        )
        essay_id = "test-model_hist-99"
        existing_path = output_dir / f"{essay_id}.txt"
        existing_path.write_text("Already generated")

        original_output_dir = generate_essays.OUTPUT_DIR
        original_get_topics = generate_essays.get_topics_by_category
        original_generate_essay = generate_essays.generate_essay

        def _fail_generate_essay(*args, **kwargs):
            raise AssertionError("generate_essay should not be called for existing files")

        try:
            generate_essays.OUTPUT_DIR = output_dir
            generate_essays.get_topics_by_category = lambda _: [topic]
            generate_essays.generate_essay = _fail_generate_essay

            essays = generate_essays.generate_essays_for_category(
                Category.HISTORICAL, models=["test-model"]
            )

            self.assertEqual(len(essays), 1)
            self.assertEqual(essays[0]["id"], essay_id)
            self.assertEqual(essays[0]["content"], "Already generated")
        finally:
            generate_essays.OUTPUT_DIR = original_output_dir
            generate_essays.get_topics_by_category = original_get_topics
            generate_essays.generate_essay = original_generate_essay
            temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()
