"""Main transcription engine for converting sheet music to solfa notation."""

from typing import List, Dict, Optional, Tuple
import numpy as np
from dataclasses import dataclass

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
        self.preprocessor = None
        self.segmenter = None 
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
        # TODO: Implement full transcription pipeline
        import cv2
        img = cv2.imread(image_path)
        cv2.imshow("Music sheet", img)
        cv2.waitKey(0)
    
    def transcribe_batch(self, image_paths: List[str]) -> List[TranscriptionResult]:
        """
        Transcribe multiple sheet music images in batch.
        
        Args:
            image_paths: List of paths to sheet music images
            
        Returns:
            List of TranscriptionResult objects
        """
        # TODO: Implement batch processing
        
    
eg_obj = TranscriptionResult()
print(eg_obj)
    

mysheet = SheetTranscriber()     
mysheet.transcribe("sheet.png")