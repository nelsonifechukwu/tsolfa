"""Unit tests for notation module."""

import pytest
from tsolfa.core.notation import SolfaConverter, SolfaNote


class TestSolfaConverter:
    """Test cases for SolfaConverter class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.converter = SolfaConverter()
    
    def test_converter_initialization(self):
        """Test converter initializes correctly."""
        assert self.converter is not None
        assert isinstance(self.converter.key_mappings, dict)
    
    def test_solfa_note_enum(self):
        """Test SolfaNote enum values."""
        assert SolfaNote.DO.value == "do"
        assert SolfaNote.RE.value == "re"
        assert SolfaNote.MI.value == "mi"
        assert SolfaNote.FA.value == "fa"
        assert SolfaNote.SO.value == "so"
        assert SolfaNote.LA.value == "la"
        assert SolfaNote.TI.value == "ti"
    
    @pytest.mark.skip("Implementation pending")
    def test_convert_to_solfa(self):
        """Test conversion from notes to solfa."""
        pass
    
    @pytest.mark.skip("Implementation pending")
    def test_format_solfa_output(self):
        """Test solfa formatting."""
        pass