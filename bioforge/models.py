from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FastaRecord:
    id: str
    description: str
    organism: str | None
    sequence: str
    line_number: int


@dataclass
class ORFCandidate:
    record_id: str
    strand: str
    frame: int
    start_pos: int
    rna_sequence: str
    is_complete: bool


@dataclass
class MotifHit:
    motif: str
    position: int


@dataclass
class ProteinSequence:
    sequence: str
    molecular_weight: float
    motif_hits: list[MotifHit] = field(default_factory=list)

    def __len__(self):
        return len(self.sequence)


@dataclass
class ORFResult:
    record_id: str
    strand: str
    frame: int
    start_pos: int
    protein: ProteinSequence
    is_complete: bool
    gc_content: float = 0.0
    bfg_id: str | None = None


@dataclass
class FilterOptions:
    min_length: int
    min_weight: float | None = None
    max_weight: float | None = None
    motifs: list[str] = field(default_factory=list)


@dataclass
class RunSummary:
    records_total: int = 0
    records_processed: int = 0
    records_skipped: int = 0
    orfs_found: int = 0
    orfs_reported: int = 0
    report_path: Path | None = None
    log_path: Path | None = None

    def log_text(self):
        return (
            f"Summary: records_total={self.records_total}, "
            f"records_processed={self.records_processed}, "
            f"records_skipped={self.records_skipped}, "
            f"orfs_found={self.orfs_found}, "
            f"orfs_reported={self.orfs_reported}"
        )
