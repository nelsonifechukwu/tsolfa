"""
TSolfa - Musical Sheet to Tonic Solfa Transcription Library

A high-performance Python library for transcribing musical sheets to solfa notation.
"""

__version__ = "0.1.0"
__author__ = "TSolfa Team"

from .core.transcription import SheetTranscriber
from .core.notation import SolfaConverter
from .vision.preprocessing import SheetPreprocessor
from .vision.segmentation import SymbolSegmenter

__all__ = [
    "SheetTranscriber",
    "SolfaConverter",
    "SheetPreprocessor",
    "SymbolSegmenter",
]