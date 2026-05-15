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
        img_no_lines = self._remove_staff_lines(binary, main_staff_lines)
        notes = self._odetect_note_heads(img_no_lines, main_staff_lines)

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
        
        #group consecutive rows Example: rows [100,101,102], store (start, end)
        main_staff_lines = []
        if staff_line_rows:
            group_start = staff_line_rows[0]
            prev_y = staff_line_rows[0]
            for y in staff_line_rows[1:]:
                if y - prev_y > 1:
                    main_staff_lines.append((group_start, prev_y))
                    group_start = y
                prev_y = y
            
            # Last group
            main_staff_lines.append((group_start, prev_y))
    
    
        staff_line_plot = np.zeros(height)
        for y_start, y_end in main_staff_lines:
            # Fill the entire range of the staff line
            for y in range(y_start, y_end + 1):
                staff_line_plot[y] = row_black_counts[y]

        # print(main_staff_lines)
        # plt.figure(figsize=(10, 5))
        # plt.plot(staff_line_plot)
        # plt.xlabel("Img height/Row (y-coordinate)")
        # plt.ylabel("Black pixel count")
        # plt.title("Detected Staff Lines")
        # plt.show()
        return staff_line_plot, main_staff_lines  # we'll process this next
        
    def _remove_staff_lines(self, binary_img, staff_lines) -> np.ndarray:
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
        for y_start, y_end in staff_lines:
            img_no_lines[y_start:y_end + 1, :] = 255  # +1 because slicing is exclusive
        
        cv2.imshow("Sheet w/o lines", img_no_lines)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return img_no_lines
    
    def _odetect_note_heads(self, img_no_lines, staff_lines):
        # Calculate expected note head size based on staff line spacing
        if len(staff_lines) >= 2:
            first_line_center = (staff_lines[0][0] + staff_lines[0][1]) // 2
            second_line_center = (staff_lines[1][0] + staff_lines[1][1]) // 2
            staff_spacing = second_line_center - first_line_center
        else:
            staff_spacing = 20
        
        print(f"Staff spacing: {staff_spacing}")
        
        min_area = (staff_spacing * 0.5) ** 2
        max_area = (staff_spacing * 2.5) ** 2
        print(f"Area range: {min_area:.1f} - {max_area:.1f}")
        
        # Invert image
        if np.mean(img_no_lines) > 127:
            img_inverted = cv2.bitwise_not(img_no_lines)
        else:
            img_inverted = img_no_lines
        
        # Find all contours
        contours, _ = cv2.findContours(img_inverted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(f"Total contours found: {len(contours)}")
        
        # DEBUG: Draw ALL contours and print their properties
        vis_img = cv2.cvtColor(img_no_lines, cv2.COLOR_GRAY2BGR)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            aspect_ratio = w / h if h > 0 else 0
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
            
            # Draw all contours in green
            cv2.rectangle(vis_img, (x, y), (x + w, y + h), (0, 0, 255), 1)
        
        # Print stats for first 20 contours
        print("\nFirst 20 contours:")
        for i, contour in enumerate(contours[:20]):
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            aspect_ratio = w / h if h > 0 else 0
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
            print(f"  {i}: area={area:.1f}, aspect={aspect_ratio:.2f}, circ={circularity:.2f}, size={w}x{h}")
        
        cv2.imshow("All contours (green)", vis_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return []
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