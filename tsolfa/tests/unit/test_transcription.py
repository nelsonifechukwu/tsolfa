"""Unit tests for transcription module."""

import pytest
from tsolfa.core.transcription import SheetTranscriber, TranscriptionResult
from tsolfa.vision.preprocessing import SheetPreprocessor
from tsolfa.vision.segmentation import SymbolSegmenter


class TestSheetTranscriber:
    """Test cases for SheetTranscriber class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transcriber = SheetTranscriber()

    def test_transcriber_initialization(self):
        """Test transcriber initializes correctly."""
        assert self.transcriber is not None
        assert isinstance(self.transcriber.preprocessor, SheetPreprocessor)
        assert isinstance(self.transcriber.segmenter, SymbolSegmenter)
        assert self.transcriber.recognizer is None
        assert self.transcriber.converter is None
    
    @pytest.mark.skip("Implementation pending")
    def test_transcribe_single_sheet(self):
        """Test transcription of a single sheet."""
        pass
    
    @pytest.mark.skip("Implementation pending") 
    def test_transcribe_batch(self):
        """Test batch transcription of multiple sheets."""
        pass