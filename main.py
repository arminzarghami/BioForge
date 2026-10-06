import argparse
import sys
from pathlib import Path

from bioforge.errors import BioForgeError
from bioforge.logging_config import setup_logging
from bioforge.models import FilterOptions
from bioforge.pipeline import run_pipeline
from bioforge.reporting import print_summary, write_report


def positive_integer(value):
    """argparse uses this function to check --min-length."""
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be an integer") from error

    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")

    return number


def non_negative_float(value):
    """Check the optional weight arguments."""
    try:
        number = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a number") from error

    if number < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")

    return number


def build_parser():
    parser = argparse.ArgumentParser(
        description="Find and analyse ORFs in a FASTA file."
    )

    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="path to the FASTA file",
    )
    parser.add_argument(
        "--out",
        required=True,
        type=Path,
        help="directory for report.txt and bioforge.log",
    )
    parser.add_argument(
        "--min-length",
        required=True,
        type=positive_integer,
        help="minimum protein length",
    )
    parser.add_argument(
        "--min-weight",
        type=non_negative_float,
        help="optional minimum protein weight",
    )
    parser.add_argument(
        "--max-weight",
        type=non_negative_float,
        help="optional maximum protein weight",
    )
    parser.add_argument(
        "--motif",
        action="append",
        default=[],
        help="protein motif; this option can be repeated",
    )

    return parser


def parse_arguments(arguments=None):
    return build_parser().parse_args(arguments)


def make_filter_options(args):
    if (
        args.min_weight is not None
        and args.max_weight is not None
        and args.min_weight > args.max_weight
    ):
        raise BioForgeError(
            "--min-weight cannot be greater than --max-weight"
        )

    motifs = []

    for item in args.motif:
        motif = item.strip().upper()

        if not motif:
            raise BioForgeError("--motif cannot be empty")

        if not motif.isalpha():
            raise BioForgeError(
                f"invalid motif {item!r}; motifs must contain letters only"
            )

        motifs.append(motif)

    return FilterOptions(
        min_length=args.min_length,
        min_weight=args.min_weight,
        max_weight=args.max_weight,
        motifs=motifs,
    )


def main(arguments=None):
    args = parse_arguments(arguments)

    # We need the output folder before logging can start.
    try:
        args.out.mkdir(parents=True, exist_ok=True)
        logger = setup_logging(args.out)
    except OSError as error:
        print(
            f"BioForge error: cannot prepare the output folder: {error}",
            file=sys.stderr,
        )
        return 2

    logger.info("BioForge run started")
    logger.info("Input file: %s", args.input)
    logger.info("Output folder: %s", args.out)

    try:
        filters = make_filter_options(args)
        results, summary = run_pipeline(args.input, filters, logger)

        summary.report_path = write_report(results, args.out)
        summary.log_path = args.out / "bioforge.log"

        print_summary(summary)
        logger.info(summary.log_text())
        logger.info("BioForge run finished successfully")
        return 0

    except (BioForgeError, OSError) as error:
        message = f"BioForge error: {error}"
        print(message, file=sys.stderr)
        logger.error(message)
        return 1

    except Exception:
        message = "BioForge stopped because of an unexpected error."
        print(message, file=sys.stderr)
        logger.exception(message)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
