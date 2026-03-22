import contextlib
import io
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import build_rules  # noqa: E402


class RepoInvariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            cls.build_status = build_rules.run_build()
        cls.build_stdout = stdout.getvalue()
        cls.build_stderr = stderr.getvalue()

        cls.report_path = ROOT / "dist" / "build-report.json"
        if cls.report_path.exists():
            cls.report = json.loads(cls.report_path.read_text(encoding="utf-8"))
        else:
            cls.report = None

    def test_run_build_succeeds(self) -> None:
        self.assertEqual(self.build_status, 0, self.build_stderr or self.build_stdout)

    def test_build_report_has_zero_warnings(self) -> None:
        self.assertIsNotNone(self.report, "缺少 dist/build-report.json")
        self.assertEqual(self.report["summary"]["total_warnings"], 0, self.report["warnings"])
        self.assertEqual(self.report["warnings"], [])

    def test_dist_only_contains_supported_output_roots(self) -> None:
        surge_root = ROOT / "dist" / "surge"
        mihomo_root = ROOT / "dist" / "mihomo"

        self.assertTrue((surge_root / "rules").is_dir())
        self.assertTrue((mihomo_root / "classical").is_dir())
        self.assertFalse((surge_root / "domainset").exists())
        self.assertFalse((mihomo_root / "domain").exists())
        self.assertFalse((mihomo_root / "ipcidr").exists())

        self.assertEqual(
            sorted(path.name for path in surge_root.iterdir() if path.is_dir()),
            ["rules"],
        )
        self.assertEqual(
            sorted(path.name for path in mihomo_root.iterdir() if path.is_dir()),
            ["classical"],
        )
