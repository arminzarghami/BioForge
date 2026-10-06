import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from bioforge.errors import (
    BioForgeError,
    DataFileError,
    FastaFormatError,
    InvalidSequenceError,
)
from bioforge.logging_config import setup_logging
from bioforge.models import (
    FastaRecord,
    FilterOptions,
    ORFCandidate,
    ORFResult,
    ProteinSequence,
)
from bioforge.pipeline import calculate_gc_content, run_pipeline, validate_sequence
from bioforge.reporting import REPORT_COLUMNS, write_report
from main import make_filter_options, parse_arguments


def make_fake_project_functions(records):
    def parse_fasta(_path):
        return records

    def load_data(_data_folder):
        codons = {"AUG": "M", "AAA": "K", "UAG": "*"}
        weights = {"M": 131.040, "K": 128.095}
        return codons, weights

    def find_orfs(sequence):
        if sequence == "ATGAAATAG":
            return [
                ORFCandidate(
                    record_id="",
                    strand="Forward",
                    frame=0,
                    start_pos=0,
                    rna_sequence="AUGAAAUAG",
                    is_complete=True,
                )
            ]

        return []

    def process_orfs(candidates, _codons, _weights, filters):
        protein = ProteinSequence("MK", 277.150)

        if len(protein) < filters.min_length:
            return []

        results = []

        for candidate in candidates:
            results.append(
                ORFResult(
                    record_id=candidate.record_id,
                    strand=candidate.strand,
                    frame=candidate.frame,
                    start_pos=candidate.start_pos,
                    protein=protein,
                    is_complete=candidate.is_complete,
                )
            )

        return results

    return parse_fasta, load_data, find_orfs, process_orfs


class CoreTests(unittest.TestCase):
    def test_exception_hierarchy(self):
        self.assertTrue(issubclass(FastaFormatError, BioForgeError))
        self.assertTrue(issubclass(InvalidSequenceError, BioForgeError))
        self.assertTrue(issubclass(DataFileError, BioForgeError))

    def test_cli_arguments(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = parse_arguments(
                [
                    "--input",
                    str(root / "input.fasta"),
                    "--out",
                    str(root / "output"),
                    "--min-length",
                    "4",
                    "--min-weight",
                    "100",
                    "--max-weight",
                    "500",
                    "--motif",
                    "mkt",
                ]
            )

            filters = make_filter_options(args)

            self.assertEqual(filters.min_length, 4)
            self.assertEqual(filters.min_weight, 100.0)
            self.assertEqual(filters.max_weight, 500.0)
            self.assertEqual(filters.motifs, ["MKT"])

    def test_log_file_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            output_folder = Path(directory)

            logger = setup_logging(output_folder)
            logger.warning("اولین اجرا")
            for handler in logger.handlers:
                handler.flush()

            logger = setup_logging(output_folder)
            logger.warning("دومین اجرا")
            for handler in logger.handlers:
                handler.flush()

            log_text = (output_folder / "bioforge.log").read_text(encoding="utf-8")

            self.assertIn("اولین اجرا", log_text)
            self.assertIn("دومین اجرا", log_text)

    def test_sequence_validation_and_gc(self):
        record = FastaRecord("seq1", "", None, "atgc", 1)
        sequence = validate_sequence(record)

        self.assertEqual(sequence, "ATGC")
        self.assertAlmostEqual(calculate_gc_content(sequence), 50.0)

        bad_record = FastaRecord("bad", "", None, "ATGNNN", 3)

        with self.assertRaises(InvalidSequenceError):
            validate_sequence(bad_record)

    def test_min_length_one_and_four(self):
        records = [FastaRecord("seq1", "", None, "ATGAAATAG", 1)]
        fake_functions = make_fake_project_functions(records)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            for min_length, expected_count in ((1, 1), (4, 0)):
                with self.subTest(min_length=min_length):
                    logger = setup_logging(root / f"output-{min_length}")

                    with patch(
                        "bioforge.pipeline.get_project_functions",
                        return_value=fake_functions,
                    ):
                        results, summary = run_pipeline(
                            root / "input.fasta",
                            FilterOptions(min_length=min_length),
                            logger,
                        )

                    self.assertEqual(len(results), expected_count)
                    self.assertEqual(summary.orfs_reported, expected_count)

                    if results:
                        self.assertEqual(results[0].bfg_id, "BFG_001")

    def test_bad_record_does_not_stop_the_next_record(self):
        records = [
            FastaRecord("bad", "", None, "ATGNNN", 1),
            FastaRecord("good", "", None, "ATGAAATAG", 3),
        ]
        fake_functions = make_fake_project_functions(records)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            logger = setup_logging(root / "output")

            with patch(
                "bioforge.pipeline.get_project_functions",
                return_value=fake_functions,
            ):
                results, summary = run_pipeline(
                    root / "input.fasta",
                    FilterOptions(min_length=1),
                    logger,
                )

            self.assertEqual(summary.records_skipped, 1)
            self.assertEqual(summary.records_processed, 1)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].record_id, "good")

    def test_empty_report_still_has_six_columns(self):
        with tempfile.TemporaryDirectory() as directory:
            report_path = write_report([], Path(directory))
            lines = report_path.read_text(encoding="utf-8").splitlines()

            self.assertEqual(lines[0].split("\t"), list(REPORT_COLUMNS))
            self.assertEqual(len(REPORT_COLUMNS), 6)
            self.assertEqual(lines[1], "No ORFs passed the active filters.")


if __name__ == "__main__":
    unittest.main()
