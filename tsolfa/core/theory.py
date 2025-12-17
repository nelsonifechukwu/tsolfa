"""Musical theory utilities and key detection."""

from typing import Dict, List, Tuple
from enum import Enum

class KeySignature(Enum):
    """
    Major key signatures. 
    All Key signatures can be intepreted as Major Keys,
    considering the outer circle of the circle of fifths
    """
    C_MAJOR = "C major"
    G_MAJOR = "G major"
    D_MAJOR = "D major" 
    A_MAJOR = "A major"
    E_MAJOR = "E major"
    B_MAJOR = "B major"
    F_SHARP_MAJOR = "F# major"
    C_SHARP_MAJOR = "C# major"
    F_MAJOR = "F major"
    B_FLAT_MAJOR = "Bb major"
    E_FLAT_MAJOR = "Eb major"
    A_FLAT_MAJOR = "Ab major"
    D_FLAT_MAJOR = "Db major"
    G_FLAT_MAJOR = "Gb major"
    C_FLAT_MAJOR = "Cb major"


class MusicalTheory:
    """Musical theory operations for key detection and note analysis."""
    
    def __init__(self):
        self.circle_of_fifths = self._initialize_circle_of_fifths()
        self.key_signatures_map = self._initialize_key_signatures()
    
    def _initialize_circle_of_fifths(self) -> List[str]:
        """Initialize the circle of fifths for key relationships."""
        return ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
    
    def _initialize_key_signatures(self) -> Dict[str, List[str]]:
        """Initialize key signature to accidentals mapping."""
    
        return {
            # Major keys with sharps
            "C major": [],
            "G major": ["F#"],
            "D major": ["F#", "C#"],
            "A major": ["F#", "C#", "G#"],
            "E major": ["F#", "C#", "G#", "D#"],
            "B major": ["F#", "C#", "G#", "D#", "A#"],
            "F# major": ["F#", "C#", "G#", "D#", "A#", "E#"],
            "C# major": ["F#", "C#", "G#", "D#", "A#", "E#", "B#"],

            # Major keys with flats
            "F major": ["Bb"],
            "Bb major": ["Bb", "Eb"],
            "Eb major": ["Bb", "Eb", "Ab"],
            "Ab major": ["Bb", "Eb", "Ab", "Db"],
            "Db major": ["Bb", "Eb", "Ab", "Db", "Gb"],
            "Gb major": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb"],
            "Cb major": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb", "Fb"],

            # Minor keys would follow same pattern...  
        }
    
    def _major_to_minor(self, major_key: KeySignature) -> str:
        """
        Convert major key to its relative minor (down a minor third).
        
        Args:
            major_key: Major key signature
            
        Returns:
            Relative minor key name
        """
        chromatic = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        major_root = major_key.value.split(" ")[0]
        
        # Handle flat notes
        if 'b' in major_root:
            flat_to_sharp = {'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#', 'Cb': 'B'}
            major_root = flat_to_sharp.get(major_root, major_root)
        
        # Relative minor is 3 semitones (minor third) down
        major_index = chromatic.index(major_root)
        minor_index = (major_index - 3) % 12
        minor_root = chromatic[minor_index]
        
        return f"{minor_root} minor"
    
    def _minor_to_major(self, minor_key: str) -> str:
        """
        Convert minor key to its relative major (up a minor third).
        
        Args:
            minor_key: Minor key name (e.g., "A minor")
            
        Returns:
            Relative major key name
        """
        chromatic = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        minor_root = minor_key.split(" ")[0]
        
        # Handle flat notes
        if 'b' in minor_root:
            flat_to_sharp = {'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#', 'Cb': 'B'}
            minor_root = flat_to_sharp.get(minor_root, minor_root)
        
        # Relative major is 3 semitones (minor third) up
        minor_index = chromatic.index(minor_root)
        major_index = (minor_index + 3) % 12
        major_root = chromatic[major_index]
        
        return f"{major_root} major"
            
    def detect_key_from_accidentals(self, sharps: int, flats: int) -> KeySignature:
        """
        Detect key signature from number of sharps/flats.
        
        Args:
            sharps: Number of sharps in key signature
            flats: Number of flats in key signature
            
        Returns:
            Detected KeySignature
        """
        # TODO: Implement key detection logic
        pass
    
    def get_scale_degrees(self, key: KeySignature) -> List[str]:
        """
        Get the scale degrees for a given key.
        
        Args:
            key: Key signature
            
        Returns:
            List of note names in the scale
        """
        # Base chromatic scale
        chromatic = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        # Major scale pattern: T-T-S-T-T-T-S (tone-tone-semitone steps)
        major_intervals = [0, 2, 4, 5, 7, 9, 11]
        major_root = key.value.split(" ")[0]
        
          # Handle accidentals in root
        if '#' in major_root:
            root_index = chromatic.index(major_root)
        elif 'b' in major_root:
            # Convert flat to sharp equivalent
            flat_to_sharp = {'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#', 'Cb': 'B'}
            root_index = chromatic.index(flat_to_sharp.get(major_root, major_root))
        else:
            root_index = chromatic.index(major_root)
        
        # Generate scale using intervals
        scale_notes = []
        for interval in major_intervals:
            note_index = (root_index + interval) % 12
            note = chromatic[note_index]
            scale_notes.append(note)
        return scale_notes
