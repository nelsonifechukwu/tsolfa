"""Solfa notation conversion utilities."""

from typing import List, Dict, Tuple
from enum import Enum

class SolfaNote(Enum):
    """Tonic solfa note names."""
    DO = "do"
    RE = "re" 
    MI = "mi"
    FA = "fa"
    SO = "so"
    LA = "la"
    TI = "ti"


class SolfaConverter:
    """Converts musical notes to solfa notation based on key signature."""
    
    def __init__(self):
        self.key_mappings = self._initialize_key_mappings()
    
    def _initialize_key_mappings(self) -> Dict[str, Dict[str, SolfaNote]]:
        """Initialize mappings from note names to solfa for each key."""
        # TODO: Implement complete key mappings
        return {}
    
    def convert_to_solfa(self, notes: List[str], key: str) -> List[SolfaNote]:
        """
        Convert note names to solfa notation for given key.
        
        Args:
            notes: List of note names (e.g., ['C', 'D', 'E'])
            key: Key signature (e.g., 'C major', 'G major')
            
        Returns:
            List of corresponding solfa notes
        """
        # TODO: Implement conversion logic
        pass
    
    def format_solfa_output(self, solfa_notes: List[SolfaNote]) -> str:
        """
        Format solfa notes into readable string notation.
        
        Args:
            solfa_notes: List of SolfaNote objects
            
        Returns:
            Formatted solfa string
        """
        # TODO: Implement formatting
        pass