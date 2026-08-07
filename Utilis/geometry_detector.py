"""
geometry_detector.py
Professional AI Book Image Enhancement Suite

Phase 2 – Step 8

Detects geometric objects in textbook images.

Author : Gangalapudi Bhasker Project
Version : 1.0
"""

from pathlib import Path
from dataclasses import dataclass
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
class GeometryResult:
    lines: int
    circles: int
    triangles: int
    rectangles: int
    polygons: int
    has_axes: bool


class GeometryDetector:

    def detect(self, image_path):

        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError("Unable to read image.")

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        blur = cv2.GaussianBlur(
            gray,
            (5, 5),
            0
        )

        edges = cv2.Canny(
            blur,
            50,
            150
        )

        # -------------------------------------
        # Detect Straight Lines
        # -------------------------------------

        lines = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            threshold=80,
            minLineLength=40,
            maxLineGap=5,
        )

        line_count = 0 if lines is None else len(lines)

        # -------------------------------------
        # Detect Circles
        # -------------------------------------

        circles = cv2.HoughCircles(
            blur,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=40,
            param1=100,
            param2=25,
            minRadius=5,
            maxRadius=300,
        )

        circle_count = (
            0 if circles is None
            else circles.shape[1]
        )

        # -------------------------------------
        # Detect Polygons
        # -------------------------------------

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        triangles = 0
        rectangles = 0
        polygons = 0

        for contour in contours:

            epsilon = (
                0.02 *
                cv2.arcLength(contour, True)
            )

            approx = cv2.approxPolyDP(
                contour,
                epsilon,
                True
            )

            sides = len(approx)

            if sides == 3:
                triangles += 1

            elif sides == 4:
                rectangles += 1

            elif sides >= 5:
                polygons += 1

        # -------------------------------------
        # Coordinate Axes Detection
        # -------------------------------------

        has_axes = False

        if line_count >= 2:

            vertical = 0
            horizontal = 0

            for l in lines:

                x1, y1, x2, y2 = l[0]

                if abs(x2 - x1) < 10:
                    vertical += 1

                if abs(y2 - y1) < 10:
                    horizontal += 1

            if (
                vertical >= 1
                and horizontal >= 1
            ):
                has_axes = True

        return GeometryResult(
            lines=line_count,
            circles=circle_count,
            triangles=triangles,
            rectangles=rectangles,
            polygons=polygons,
            has_axes=has_axes,
        )

    # -----------------------------------------

    def scan_folder(self, folder):

        folder = Path(folder)

        results = {}

        for ext in SUPPORTED:

            for img in folder.glob(f"*{ext}"):

                results[img.name] = self.detect(img)

        return results


# ---------------------------------------------

if __name__ == "__main__":

    detector = GeometryDetector()

    results = detector.scan_folder(
        "enhanced"
    )

    for name, r in results.items():

        print()

        print(name)

        print(r)
