REPORT_COLUMNS = (
    "ID",
    "Strand",
    "Frame",
    "Start Position",
    "Protein",
    "Complete / Incomplete",
)


def write_report(results, output_folder):
    output_folder.mkdir(parents=True, exist_ok=True)
    report_path = output_folder / "report.txt"

    # The report is replaced on each run. Only the log file uses append mode.
    with report_path.open("w", encoding="utf-8") as report_file:
        report_file.write("\t".join(REPORT_COLUMNS) + "\n")

        if not results:
            report_file.write("No ORFs passed the active filters.\n")
            return report_path

        for result in results:
            status = "Complete" if result.is_complete else "Incomplete"

            row = [
                result.bfg_id,
                result.strand,
                str(result.frame),
                str(result.start_pos),
                result.protein.sequence,
                status,
            ]

            report_file.write("\t".join(row) + "\n")

    return report_path


def print_summary(summary):
    print("BioForge completed successfully.")
    print(
        f"Records: {summary.records_total} total, "
        f"{summary.records_processed} processed, "
        f"{summary.records_skipped} skipped"
    )
    print(
        f"ORFs: {summary.orfs_found} found, "
        f"{summary.orfs_reported} written to the report"
    )
    print(f"Report: {summary.report_path}")
    print(f"Log: {summary.log_path}")
