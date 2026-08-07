"""
image_classifier.py
Professional AI Book Image Enhancement Suite

Phase 2 - Step 7

Rule-based Image Classifier
(Ready to be replaced by AI model in future)

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
class ClassificationResult:
    label: str
    confidence: float


class ImageClassifier:

    def __init__(self):
        pass

    def classify(self, image_path):

        image = cv2.imread(str(image_path))

        if image is None:
            return ClassificationResult(
                "unknown",
                0.0
            )

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        edges = cv2.Canny(
            gray,
            100,
            200
        )

        edge_ratio = np.count_nonzero(edges) / edges.size

        lines = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            80,
            minLineLength=40,
            maxLineGap=5,
        )

        line_count = 0 if lines is None else len(lines)

        brightness = gray.mean()

        unique_colors = len(
            np.unique(
                image.reshape(-1, 3),
                axis=0
            )
        )

        # -------- Geometry --------

        if line_count > 80 and edge_ratio > 0.12:
            return ClassificationResult(
                "geometry",
                0.90
            )

        # -------- Graph --------

        if (
            line_count > 30
            and edge_ratio > 0.06
        ):
            return ClassificationResult(
                "graph",
                0.82
            )

        # -------- Table --------

        if (
            line_count > 120
            and brightness > 180
        ):
            return ClassificationResult(
                "table",
                0.86
            )

        # -------- Photo --------

        if unique_colors > 5000:
            return ClassificationResult(
                "photo",
                0.88
            )

        # -------- Mixed --------

        if (
            edge_ratio > 0.03
            and unique_colors > 1000
        ):
            return ClassificationResult(
                "mixed",
                0.75
            )

        return ClassificationResult(
            "unknown",
            0.50
        )

    # ------------------------------------------------

    def classify_folder(self, folder):

        folder = Path(folder)

        results = {}

        for ext in SUPPORTED:

            for img in folder.glob(f"*{ext}"):

                results[img.name] = self.classify(img)

        return results


# ----------------------------------------------------

if __name__ == "__main__":

    classifier = ImageClassifier()

    results = classifier.classify_folder(
        "enhanced"
    )

    print()

    for file, result in results.items():

        print(
            f"{file:25s}"
            f"{result.label:12s}"
            f"{result.confidence:.2f}"
        )
