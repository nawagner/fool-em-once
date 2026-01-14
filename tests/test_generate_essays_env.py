import os
import sys
import unittest
from pathlib import Path


class GenerateEssaysEnvTest(unittest.TestCase):
    def setUp(self):
        self.old_env = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.old_env)

    def test_get_api_key_accepts_hyphen_name(self):
        os.environ.pop("OPENROUTER_API_KEY", None)
        os.environ["OPENROUTER-API-KEY"] = "hyphen-key"

        repo_root = Path(__file__).resolve().parents[1]
        sys.path.insert(0, str(repo_root / "src"))

        import generate_essays  # noqa: E402

        self.assertEqual(generate_essays.get_api_key(), "hyphen-key")


if __name__ == "__main__":
    unittest.main()
