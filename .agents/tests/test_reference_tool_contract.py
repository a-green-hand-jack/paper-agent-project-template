from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

try:
    from bibtex_updater.utils import HttpClient, RateLimiter, SqliteCache
except ImportError:
    HttpClient = None

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / ".agents/scripts/_bounded_run.py"


@unittest.skipIf(HttpClient is None, "bibtex-updater is installed only in the locked reference environment")
class LockedToolContractTests(unittest.TestCase):
    """The audits write the locked tool's cache directly; a lock upgrade that
    changes its circuit state or cache table fails here, not in a paper's CI."""

    def test_keyless_openalex_skip_opens_the_tool_circuit(self) -> None:
        spec = importlib.util.spec_from_file_location("paper_bounded_run", HELPER)
        assert spec is not None and spec.loader is not None
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        self.assertEqual(helper.CIRCUIT_KEY, HttpClient._CIRCUIT_CACHE_KEY)
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "metadata.db"
            for keyless in (True, False):
                with self.subTest(keyless=keyless):
                    environment = {} if keyless else {"OPENALEX_API_KEY": "fixture-key"}
                    helper.skip_keyless_openalex(database, environment, 600)
                    client = HttpClient(timeout=1, user_agent="contract-test", rate_limiter=RateLimiter(60),
                                        cache=SqliteCache(str(database)))
                    self.assertEqual(client._circuit_is_open("openalex"), keyless)
                    self.assertFalse(client._circuit_is_open("crossref"))


if __name__ == "__main__":
    unittest.main()
