"""
report_generator.py
Professional AI Book Image Enhancement Suite

Phase 1 – Step 6
Processing Report Generator

Author : Gangalapudi Bhasker Project
Version : 1.0
"""

from pathlib import Path
from PIL import Image
import pandas as pd
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
    ".bmp",
    ".webp",
)


class ReportGenerator:

    def __init__(self):
        pass

    def generate(
        self,
        image_dir,
        output_csv="reports/report.csv",
    ):

        image_dir = Path(image_dir)

        output_csv = Path(output_csv)

        output_csv.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        rows = []

        images = []

        for ext in SUPPORTED:
            images.extend(
                image_dir.glob(f"*{ext}")
            )

        images = sorted(images)

        logging.info(
            "Scanning %d images...",
            len(images)
        )

        for img in images:

            try:

                im = Image.open(img)

                width, height = im.size

                rows.append({

                    "Filename":
                        img.name,

                    "Width":
                        width,

                    "Height":
                        height,

                    "Format":
                        im.format,

                    "Mode":
                        im.mode,

                    "File Size (KB)":
                        round(
                            img.stat().st_size / 1024,
                            2
                        )

                })

            except Exception as e:

                rows.append({

                    "Filename":
                        img.name,

                    "Error":
                        str(e)

                })

        df = pd.DataFrame(rows)

        df.to_csv(
            output_csv,
            index=False
        )

        logging.info(
            "Report Saved : %s",
            output_csv
        )

        print()

        print("=" * 60)

        print("SUMMARY")

        print("=" * 60)

        print("Images :", len(df))

        print("CSV    :", output_csv)

        print("=" * 60)


if __name__ == "__main__":

    report = ReportGenerator()

    report.generate(

        image_dir="final_images",

        output_csv="reports/report.csv"

    )
