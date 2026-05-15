"""Image preprocessing for sheet music analysis."""

from typing import List, Tuple

import cv2
import numpy as np


class SheetPreprocessor:
    """Preprocesses sheet music images for symbol recognition."""

    def __init__(self, debug: bool = False):
        self.debug = debug

    def binarize(self, image_path: str) -> np.ndarray:
        """Load a grayscale image and apply Otsu thresholding."""
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    def detect_staff_lines(
        self, binary_img: np.ndarray
    ) -> Tuple[np.ndarray, List[Tuple[int, int]]]:
        """
        Detect staff lines from a binary image.

        Returns:
            staff_line_plot: per-row black-pixel counts, restricted to rows
                that belong to a detected staff line (useful for debugging).
            main_staff_lines: list of (y_start, y_end) bands, one per line.
        """
        height, width = binary_img.shape

        row_black_counts = []
        for y in range(height):
            row = binary_img[y, :]
            black_count = np.sum(row == 0)
            row_black_counts.append(black_count)

        staff_line_threshold = width * 0.5  # staff lines span > 0.5 width
        staff_line_rows = [
            y for y, black_count in enumerate(row_black_counts)
            if black_count > staff_line_threshold
        ]

        # Group consecutive rows. Example: [100,101,102] -> (100, 102)
        main_staff_lines: List[Tuple[int, int]] = []
        if staff_line_rows:
            group_start = staff_line_rows[0]
            prev_y = staff_line_rows[0]
            for y in staff_line_rows[1:]:
                if y - prev_y > 1:
                    main_staff_lines.append((group_start, prev_y))
                    group_start = y
                prev_y = y
            main_staff_lines.append((group_start, prev_y))

        staff_line_plot = np.zeros(height)
        for y_start, y_end in main_staff_lines:
            for y in range(y_start, y_end + 1):
                staff_line_plot[y] = row_black_counts[y]

        return staff_line_plot, main_staff_lines

    def remove_staff_lines(
        self, binary_img: np.ndarray, staff_lines: List[Tuple[int, int]]
    ) -> np.ndarray:
        """Whiten the staff-line bands so notes can be isolated."""
        img_no_lines = binary_img.copy()
        for y_start, y_end in staff_lines:
            img_no_lines[y_start:y_end + 1, :] = 255

        if self.debug:
            cv2.imshow("Sheet w/o lines", img_no_lines)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return img_no_lines
