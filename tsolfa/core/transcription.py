"""Main transcription engine for converting sheet music to solfa notation."""

from dataclasses import dataclass
from typing import List, Tuple

from ..vision.preprocessing import SheetPreprocessor
from ..vision.segmentation import SymbolSegmenter


@dataclass
class TranscriptionResult:
    """Result of sheet music transcription."""
    solfa_notation: List[str] = None
    key_signature: str = ""
    time_signature: Tuple[int, int] = ()
    confidence_score: float = 0.0
    processing_time: float = 0.0


class SheetTranscriber:
    """High-performance sheet music to solfa transcriber."""

    def __init__(self):
        self.preprocessor = SheetPreprocessor()
        self.segmenter = SymbolSegmenter()
        self.recognizer = None
        self.converter = None

    def transcribe(self, image_path: str) -> TranscriptionResult:
        """
        Transcribe sheet music image to solfa notation.

        Args:
            image_path: Path to sheet music image

        Returns:
            TranscriptionResult with solfa notation and metadata
        """
        binary = self.preprocessor.binarize(image_path)
        _, main_staff_lines = self.preprocessor.detect_staff_lines(binary)
        img_no_lines = self.preprocessor.remove_staff_lines(binary, main_staff_lines)
        notes = self.segmenter.detect_note_heads(img_no_lines, main_staff_lines)

    def transcribe_batch(self, image_paths: List[str]) -> List[TranscriptionResult]:
        """
        Transcribe multiple sheet music images in batch.

        Args:
            image_paths: List of paths to sheet music images

        Returns:
            List of TranscriptionResult objects
        """
        # TODO: Implement batch processing