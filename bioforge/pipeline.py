from pathlib import Path

from bioforge.errors import FastaFormatError, InvalidSequenceError
from bioforge.models import RunSummary


VALID_DNA_BASES = set("ACGT")


def get_project_functions():
    """Import the functions written by the other team members."""
    try:
        from bioforge.data import load_data
        from bioforge.fasta import parse_fasta
        from bioforge.orf import find_orfs
        from bioforge.processing import process_orfs
    except ImportError as error:
        raise RuntimeError(
            "One of the project modules has not been added yet. "
            "Check fasta.py, data.py, orf.py and processing.py."
        ) from error

    return parse_fasta, load_data, find_orfs, process_orfs


def validate_sequence(record):
    sequence = record.sequence.strip().upper()

    if not sequence:
        raise FastaFormatError(
            f"record {record.id!r} at line {record.line_number} has no sequence"
        )

    invalid_characters = sorted(set(sequence) - VALID_DNA_BASES)

    if invalid_characters:
        characters = ", ".join(repr(char) for char in invalid_characters)
        raise InvalidSequenceError(
            f"record {record.id!r} contains invalid character(s): {characters}"
        )

    return sequence


def calculate_gc_content(sequence):
    gc_count = sequence.count("G") + sequence.count("C")
    return gc_count / len(sequence) * 100


def warn_about_duplicate_ids(records, logger):
    seen_ids = set()

    for record in records:
        if record.id in seen_ids:
            logger.warning("Duplicate FASTA ID kept: %s", record.id)

        seen_ids.add(record.id)


def add_record_information(results, record, gc_content):
    for result in results:
        if not result.record_id:
            result.record_id = record.id

        result.gc_content = gc_content


def assign_bfg_ids(results):
    # IDs are created after filtering so there are no gaps in the report.
    for number, result in enumerate(results, start=1):
        result.bfg_id = f"BFG_{number:03d}"


def run_pipeline(input_path, filters, logger):
    parse_fasta, load_data, find_orfs, process_orfs = get_project_functions()

    project_root = Path(__file__).resolve().parent.parent
    data_folder = project_root / "data"

    # Data-file errors are global errors, so they are not caught in the record loop.
    codon_table, amino_weights = load_data(data_folder)

    records = list(parse_fasta(input_path))

    if not records:
        raise FastaFormatError(f"FASTA file is empty or has no valid records: {input_path}")

    warn_about_duplicate_ids(records, logger)

    summary = RunSummary(records_total=len(records))
    selected_orfs = []

    for record in records:
        try:
            sequence = validate_sequence(record)
            gc_content = calculate_gc_content(sequence)

            logger.info(
                "Processing record %s (length=%d, GC=%.2f%%)",
                record.id,
                len(sequence),
                gc_content,
            )

            candidates = list(find_orfs(sequence))
            summary.orfs_found += len(candidates)

            for candidate in candidates:
                if not candidate.record_id:
                    candidate.record_id = record.id

            record_results = list(
                process_orfs(
                    candidates,
                    codon_table,
                    amino_weights,
                    filters,
                )
            )

            add_record_information(record_results, record, gc_content)
            selected_orfs.extend(record_results)
            summary.records_processed += 1

        except (FastaFormatError, InvalidSequenceError) as error:
            summary.records_skipped += 1
            logger.warning("Skipped record %s: %s", record.id, error)

    assign_bfg_ids(selected_orfs)
    summary.orfs_reported = len(selected_orfs)

    return selected_orfs, summary
