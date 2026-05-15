"""Main transcription engine for converting sheet music to solfa notation."""

from dataclasses import dataclass
from typing import List, Tuple

import cv2
import numpy as np

from ..vision.preprocessing import SheetPreprocessor


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
        binary = self.preprocessor.binarize(image_path)
        _, main_staff_lines = self.preprocessor.detect_staff_lines(binary)
        img_no_lines = self.preprocessor.remove_staff_lines(binary, main_staff_lines)
        notes = self._detect_note_heads(img_no_lines, main_staff_lines)

    def _detect_note_heads(self, img_no_lines, staff_lines):
        # Calculate staff spacing
        if len(staff_lines) >= 2:
            first_line_center = (staff_lines[0][0] + staff_lines[0][1]) // 2
            second_line_center = (staff_lines[1][0] + staff_lines[1][1]) // 2
            staff_spacing = second_line_center - first_line_center
        else:
            staff_spacing = 20
        
        print(f"Staff spacing: {staff_spacing}")
        
        # Invert image (we need white objects on black background)
        if np.mean(img_no_lines) > 127:
            img_inverted = cv2.bitwise_not(img_no_lines)
        else:
            img_inverted = img_no_lines
        
        # REPAIR: Use morphological closing to reconnect broken note heads
        kernel_size = max(3, staff_spacing // 4)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        img_closed = cv2.morphologyEx(img_inverted, cv2.MORPH_CLOSE, kernel)
        
        # Show the repaired image
        cv2.imshow("After morphological closing", img_closed)
        cv2.waitKey(0)
        
        # Now find contours on the repaired image
        contours, _ = cv2.findContours(img_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(f"Total contours found: {len(contours)}")
        
        min_area = (staff_spacing * 0.5) ** 2
        max_area = (staff_spacing * 3.0) ** 2
        
        note_heads = []
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            
            if area < min_area or area > max_area:
                continue
            
            aspect_ratio = w / h if h > 0 else 0
            if aspect_ratio < 0.5 or aspect_ratio > 2.5:
                continue
            
            perimeter = cv2.arcLength(contour, True)
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter ** 2)
                if circularity < 0.4:
                    continue
            
            center_x = x + w // 2
            center_y = y + h // 2
            note_heads.append((center_x, center_y, w, h))
        
        note_heads.sort(key=lambda n: n[0])
        
        # Visualize detections
        vis_img = cv2.cvtColor(img_no_lines, cv2.COLOR_GRAY2BGR)
        for (cx, cy, w, h) in note_heads:
            x = cx - w // 2
            y = cy - h // 2
            cv2.rectangle(vis_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        cv2.imshow(f"Detected {len(note_heads)} note heads", vis_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        print(f"Found {len(note_heads)} note heads")
        return note_heads

    def transcribe_batch(self, image_paths: List[str]) -> List[TranscriptionResult]:
        """
        Transcribe multiple sheet music images in batch.

        Args:
            image_paths: List of paths to sheet music images

        Returns:
            List of TranscriptionResult objects
        """
        # TODO: Implement batch processing