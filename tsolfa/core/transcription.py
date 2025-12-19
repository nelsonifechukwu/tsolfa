"""Main transcription engine for converting sheet music to solfa notation."""

from typing import List, Dict, Optional, Tuple
import numpy as np
import cv2
import matplotlib.pyplot as plt 
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

        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # img = cv2.medianBlur(img,9) -> for img with different lightning conditions
        #_, binary3 = cv2.threshold(img, 200, 255,  cv2.THRESH_BINARY)
        #binary2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        _,binary = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        # cv2.imshow("Grayscale", img)
        # cv2.imshow("Binary", binary)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        _ , main_staff_lines = self._detect_staff_lines(binary)
        _ = self._remove_staff_lines(binary, main_staff_lines)

    def _detect_staff_lines(self, binary_img):
        """
        Detect staff lines from binary image.
        
        Returns:
            list of y-coordinates for each staff line
        """
        height, width = binary_img.shape
        
        # Count black pixels (value 0) in each row
        row_black_counts = []
        for y in range(height):
            row = binary_img[y, :]
            black_count = np.sum(row==0)  # count pixels that equal 0
            row_black_counts.append(black_count)
        
        # let's visualize where staff lines are
        staff_line_threshold = width * 0.5 #staff lines span > 0.5 width
        staff_line_rows = [y for y, black_count in enumerate(row_black_counts) if black_count > staff_line_threshold]
        
        #group consecutive rows into single lines
        #Example: rows [100,101,102] become single line at y=101
        main_staff_lines = []
        if staff_line_rows:
            group_start = staff_line_rows[0]
            prev_y = staff_line_rows[0]
            
            for y in staff_line_rows[1:]:
                if y - prev_y > 1:  # gap means new line    
                    # End current group, save center position
                    line_thickness = prev_y - group_start
                    center = (group_start + prev_y) // 2
                    main_staff_lines.append((center, line_thickness))
                    group_start = y
                prev_y = y
            
            # Don't forget the last group!
            line_thickness = prev_y - group_start
            center = (group_start + prev_y) // 2
            main_staff_lines.append((center, line_thickness))
    
    
        # Create an array of zeros for the full image height
        staff_line_plot = np.zeros(height)
        # Mark only the detected staff line positions with their counts
        for y, _ in main_staff_lines:
            staff_line_plot[y] = row_black_counts[y]

        # plt.figure(figsize=(10, 5))
        # plt.plot(staff_line_plot)
        # plt.xlabel("Img height/Row (y-coordinate)")
        # plt.ylabel("Black pixel count")
        # plt.title("Detected Staff Lines")
        # plt.show()
        return staff_line_plot, main_staff_lines  # we'll process this next
        
    def _remove_staff_lines(self, binary_img, staff_lines):
        """
        Remove staff lines from image to isolate notes.
        
        Args:
            binary_img: Binary image
            staff_lines: List of y-coordinates of staff line centers
            line_thickness: How many pixels above/below center to remove
        
        Returns:
            Image with staff lines removed
        """
        # Make a copy so we don't modify the original
        img_no_lines = binary_img.copy()
        
        for y, line_thickness in staff_lines:
            # Set rows around each staff line to white (255)
            y_start = y-(line_thickness//2)
            y_end = y+(line_thickness//2)+1
            img_no_lines[y_start:y_end, :] = 255
        
        cv2.imshow("Sheet w/o lines", img_no_lines)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return img_no_lines
            
    def transcribe_batch(self, image_paths: List[str]) -> List[TranscriptionResult]:
        """
        Transcribe multiple sheet music images in batch.
        
        Args:
            image_paths: List of paths to sheet music images
            
        Returns:
            List of TranscriptionResult objects
        """
        # TODO: Implement batch processing
        

mysheet = SheetTranscriber()     
mysheet.transcribe("/Users/elijahnelson/Desktop/PROJECTS/tsolfa/tsolfa/data/sheets/sheet.png")