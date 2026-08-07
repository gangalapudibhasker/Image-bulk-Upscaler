"""
pdf_rebuilder.py
Professional AI Book Image Enhancement Suite

Phase 1 – Step 5
Rebuild PDF from Enhanced Images

Author : Gangalapudi Bhasker Project
Version : 1.0
"""

from pathlib import Path
import img2pdf
from PIL import Image
from tqdm import tqdm
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

SUPPORTED = (
    ".png",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
)


class PDFRebuilder:

    def __init__(self):
        pass

    def build_pdf(
        self,
        input_dir,
        output_pdf,
    ):

        input_dir = Path(input_dir)
        output_pdf = Path(output_pdf)

        output_pdf.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        images = []

        for ext in SUPPORTED:
            images.extend(input_dir.glob(f"*{ext}"))

        images = sorted(images)

        if len(images) == 0:
            raise ValueError(
                "No images found."
            )

        logging.info(
            "Images Found : %d",
            len(images)
        )

        image_list = []

        for img in tqdm(images):

            image = Image.open(img)

            if image.mode == "RGBA":
                image = image.convert("RGB")
                image.save(img)

            image_list.append(str(img))

        with open(output_pdf, "wb") as f:

            f.write(
                img2pdf.convert(
                    image_list
                )
            )

        logging.info(
            "PDF Created Successfully."
        )

        logging.info(
            "Saved To : %s",
            output_pdf
        )


if __name__ == "__main__":

    builder = PDFRebuilder()

    builder.build_pdf(
        input_dir="final_images",
        output_pdf="output/enhanced_book.pdf",
    )
