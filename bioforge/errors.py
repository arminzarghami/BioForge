"""Custom exception hierarchy used throughout BioForge."""


class BioForgeError(Exception):
    """Base class for expected BioForge errors."""


class FastaFormatError(BioForgeError):
    """Raised when a FASTA file or record has an invalid structure."""


class InvalidSequenceError(BioForgeError):
    """Raised when a DNA sequence contains characters other than A/C/G/T."""


class DataFileError(BioForgeError):
    """Raised when a shared reference-data file is missing or malformed."""
