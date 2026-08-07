"""
graph_detector.py
Professional AI Book Image Enhancement Suite

Phase 2 – Step 9

Detects graphs and charts in textbook images.

Author : Gangalapudi Bhasker Project
Version : 1.0
"""

from dataclasses import dataclass
from pathlib import Path
import cv2
import numpy as np


SUPPORTED = (
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tif",
    ".tiff",
)


@dataclass
class GraphResult:

    vertical_lines: int
    horizontal_lines: int

    bars: int

    circles: int

    grid_detected: bool

    graph_type: str


class GraphDetector:

    def detect(self, image_path):

        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError("Cannot read image.")

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        edges = cv2.Canny(
            gray,
            50,
            150
        )

        lines = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            80,
            minLineLength=50,
            maxLineGap=5
        )

        vertical = 0
        horizontal = 0

        if lines is not None:

            for line in lines:

                x1, y1, x2, y2 = line[0]

                if abs(x2 - x1) < 8:
                    vertical += 1

                elif abs(y2 - y1) < 8:
                    horizontal += 1

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        bars = 0

        for c in contours:

            x, y, w, h = cv2.boundingRect(c)

            area = w * h

            if area < 500:
                continue

            if h > w * 2:
                bars += 1

        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            1.2,
            30
        )

        circle_count = (
            0 if circles is None
            else circles.shape[1]
        )

        grid = (
            vertical > 5
            and horizontal > 5
        )

        graph_type = "unknown"

        if bars >= 3:

            graph_type = "bar_graph"

        elif grid:

            graph_type = "coordinate_graph"

        elif circle_count >= 1:

            graph_type = "pie_chart"

        return GraphResult(
            vertical_lines=vertical,
            horizontal_lines=horizontal,
            bars=bars,
            circles=circle_count,
            grid_detected=grid,
            graph_type=graph_type
        )

    def scan_folder(self, folder):

        folder = Path(folder)

        results = {}

        for ext in SUPPORTED:

            for img in folder.glob(f"*{ext}"):

                results[img.name] = self.detect(img)

        return results


if __name__ == "__main__":

    detector = GraphDetector()

    results = detector.scan_folder(
        "enhanced"
    )

    for file, result in results.items():

        print(file)

        print(result)

        print()
