"""Tests unitarios mínimos para KeywordResearchTool (fallback CSV)."""

import os
import tempfile
import unittest
from pathlib import Path

from direttorio.tools.keyword_research_tool import KeywordResearchTool


class TestKeywordResearchTool(unittest.TestCase):
    def setUp(self):
        self._saved_env = {}
        for k in ("SEMRUSH_API_KEY", "KEYWORDS_CSV"):
            self._saved_env[k] = os.environ.get(k)

    def tearDown(self):
        for k, v in self._saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_keyword_research_csv_fallback(self):
        """Sin SEMRUSH_API_KEY, la herramienta lee de KEYWORDS_CSV y retorna tabla markdown."""
        with tempfile.TemporaryDirectory() as d:
            csv_path = Path(d) / "keywords.csv"
            csv_path.write_text(
                "keyword,volume,cpc,competition\n"
                "ejemplo keyword 1,3200,0.5,medium\n"
                "ejemplo keyword 2,1100,0.3,low\n",
                encoding="utf-8",
            )
            os.environ["KEYWORDS_CSV"] = str(csv_path)
            os.environ.pop("SEMRUSH_API_KEY", None)

            tool = KeywordResearchTool()
            result = tool._run(query="ejemplo", database="us")

        self.assertIn("## Investigación de keywords", result)
        self.assertIn("| Keyword |", result)
        self.assertIn("ejemplo", result.lower())
        self.assertTrue("3200" in result or "0.5" in result)

    def test_keyword_research_csv_missing_file(self):
        """Cuando el CSV falta, retorna mensaje útil."""
        os.environ["KEYWORDS_CSV"] = "nonexistent/keywords.csv"
        os.environ.pop("SEMRUSH_API_KEY", None)

        tool = KeywordResearchTool()
        result = tool._run(query="test", database="us")

        self.assertIn("No hay CSV de keywords", result)
        self.assertTrue(
            "knowledge/keywords.csv" in result
            or "KEYWORDS_CSV" in result
            or "nonexistent" in result
        )


if __name__ == "__main__":
    unittest.main()
