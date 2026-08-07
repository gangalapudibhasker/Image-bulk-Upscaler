"""
image_enhancer.py
Professional AI Book Image Enhancement Suite

Phase 1 – Step 4

Author : Gangalapudi Bhasker Project
Version : 1.0
"""

from pathlib import Path
import logging

import cv2
import numpy as np
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

SUPPORTED_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
)


class ImageEnhancer:
    """
    Batch Image Enhancement Engine
    """

    def __init__(
        self,
        sharpen=True,
        denoise=True,
        contrast=True,
        remove_border=True,
    ):

        self.sharpen = sharpen
        self.denoise = denoise
        self.contrast = contrast
        self.remove_border = remove_border

    # ---------------------------------------------------

    def enhance_folder(
        self,
        input_dir,
        output_dir,
    ):

        input_dir = Path(input_dir)
        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        images = []

        for ext in SUPPORTED_EXTENSIONS:
            images.extend(input_dir.glob(f"*{ext}"))

        images = sorted(images)

        logging.info("Images Found : %d", len(images))

        for image_path in tqdm(images):

            image = cv2.imread(str(image_path))

            if image is None:
                continue

            image = self.process(image)

            cv2.imwrite(
                str(output_dir / image_path.name),
                image
            )

        logging.info("Enhancement Completed.")

    # ---------------------------------------------------

    def process(self, image):

        if self.remove_border:
            image = self.crop_white_border(image)

        if self.denoise:
            image = self.apply_denoise(image)

        if self.contrast:
            image = self.apply_clahe(image)

        if self.sharpen:
            image = self.apply_sharpen(image)

        return image

    # ---------------------------------------------------

    @staticmethod
    def apply_denoise(image):

        return cv2.fastNlMeansDenoisingColored(
            image,
            None,
            5,
            5,
            7,
            21,
        )

    # ---------------------------------------------------

    @staticmethod
    def apply_clahe(image):

        lab = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2LAB
        )

        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8),
        )

        l = clahe.apply(l)

        lab = cv2.merge((l, a, b))

        return cv2.cvtColor(
            lab,
            cv2.COLOR_LAB2BGR
        )

    # ---------------------------------------------------

    @staticmethod
    def apply_sharpen(image):

        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0],
        ])

        return cv2.filter2D(
            image,
            -1,
            kernel,
        )

    # ---------------------------------------------------

    @staticmethod
    def crop_white_border(image):

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        _, thresh = cv2.threshold(
            gray,
            245,
            255,
            cv2.THRESH_BINARY_INV,
        )

        coords = cv2.findNonZero(thresh)

        if coords is None:
            return image

        x, y, w, h = cv2.boundingRect(coords)

        return image[y:y + h, x:x + w]


# -------------------------------------------------------

if __name__ == "__main__":

    enhancer = ImageEnhancer()

    enhancer.enhance_folder(
        input_dir="enhanced",
        output_dir="final_images",
    )
