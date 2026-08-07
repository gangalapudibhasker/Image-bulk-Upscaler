"""
photo_detector.py
Professional AI Book Image Enhancement Suite

Phase 2 - Step 10

Detects photographs, illustrations and scanned images.

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
    ".webp",
)


@dataclass
class PhotoResult:
    image_type: str
    confidence: float
    colorful: bool
    photo_score: float
    edge_density: float


class PhotoDetector:

    def detect(self, image_path):

        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError("Unable to load image.")

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        hsv = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2HSV
        )

        # ---------------------------------
        # Colorfulness
        # ---------------------------------

        std_saturation = hsv[:, :, 1].std()

        colorful = std_saturation > 30

        # ---------------------------------
        # Edge Density
        # ---------------------------------

        edges = cv2.Canny(
            gray,
            80,
            180
        )

        edge_density = (
            np.count_nonzero(edges)
            / edges.size
        )

        # ---------------------------------
        # Unique Colors
        # ---------------------------------

        unique_colors = len(
            np.unique(
                image.reshape(-1, 3),
                axis=0
            )
        )

        # ---------------------------------
        # Texture
        # ---------------------------------

        texture = gray.std()

        # ---------------------------------
        # Photo Score
        # ---------------------------------

        score = 0

        if colorful:
            score += 30

        if unique_colors > 5000:
            score += 30

        if texture > 35:
            score += 20

        if edge_density < 0.15:
            score += 20

        score = min(score, 100)

        # ---------------------------------
        # Classification
        # ---------------------------------

        if score >= 80:

            label = "photo"

        elif score >= 60:

            label = "illustration"

        elif score >= 40:

            label = "cartoon"

        else:

            label = "diagram"

        confidence = score / 100

        return PhotoResult(
            image_type=label,
            confidence=confidence,
            colorful=colorful,
            photo_score=score,
            edge_density=edge_density
        )

    # -------------------------------------

    def scan_folder(self, folder):

        folder = Path(folder)

        results = {}

        for ext in SUPPORTED:

            for img in folder.glob(f"*{ext}"):

                results[img.name] = self.detect(img)

        return results


# ------------------------------------------

if __name__ == "__main__":

    detector = PhotoDetector()

    results = detector.scan_folder(
        "enhanced"
    )

    print()

    for name, result in results.items():

        print(name)

        print(result)

        print()
