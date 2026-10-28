import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from parse_ptp_logs import parse_lines, summarize  # noqa: E402


class ParseLinesTests(unittest.TestCase):
    def test_parses_positive_and_negative_offsets(self):
        lines = [
            "ptp4l[123.0]: master offset -10 s2 freq +3 path delay 100\n",
            "ptp4l[124.0]: master offset +20 s2 freq -1 path delay 120\n",
        ]
        records, unmatched = parse_lines(lines)
        self.assertEqual(
            records,
            [
                {"offset_ns": -10, "path_delay_ns": 100},
                {"offset_ns": 20, "path_delay_ns": 120},
            ],
        )
        self.assertEqual(unmatched, 0)

    def test_counts_unmatched_nonempty_lines(self):
        records, unmatched = parse_lines(
            ["\n", "startup message\n", "master offset -1 s2 freq +0 path delay 3\n"]
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(unmatched, 1)

    def test_summary_values(self):
        records = [
            {"offset_ns": -10, "path_delay_ns": 100},
            {"offset_ns": 10, "path_delay_ns": 200},
        ]
        summary = summarize(records)
        self.assertEqual(summary["sample_count"], 2)
        self.assertEqual(summary["mean_offset_ns"], 0)
        self.assertAlmostEqual(summary["rms_offset_ns"], 10)
        self.assertEqual(summary["max_abs_offset_ns"], 10)
        self.assertEqual(summary["mean_path_delay_ns"], 150)

    def test_empty_summary_raises(self):
        with self.assertRaises(ValueError):
            summarize([])


if __name__ == "__main__":
    unittest.main()
