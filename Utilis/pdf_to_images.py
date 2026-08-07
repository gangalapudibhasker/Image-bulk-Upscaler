"""
pdf_to_images.py
----------------
Professional AI Book Image Enhancement Suite
Phase 1 - Step 2

Converts a PDF into high-resolution page images.

Author : Gangalapudi Bhasker Project
Version: 1.0
"""

from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF
from tqdm import tqdm


def pdf_to_images(
    pdf_path: str,
    output_dir: str,
    dpi: int = 600,
    image_format: str = "png",
    start_page: int = 1,
    end_page: Optional[int] = None,
) -> int:
    """
    Convert PDF pages to high-resolution images.

    Parameters
    ----------
    pdf_path : str
        Input PDF file.

    output_dir : str
        Folder where images will be saved.

    dpi : int
        Output resolution.
        Recommended: 300 or 600.

    image_format : str
        png / jpg

    start_page : int
        First page (1-based).

    end_page : int
        Last page (inclusive).
        None = all pages.

    Returns
    -------
    int
        Number of exported pages.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found:\n{pdf_path}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    document = fitz.open(pdf_path)

    total_pages = len(document)

    if end_page is None:
        end_page = total_pages

    start_page = max(1, start_page)
    end_page = min(total_pages, end_page)

    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    print("=" * 60)
    print("PDF TO IMAGES")
    print("=" * 60)
    print(f"Input PDF   : {pdf_path}")
    print(f"Pages       : {total_pages}")
    print(f"DPI         : {dpi}")
    print(f"Output      : {output_dir}")
    print("=" * 60)

    exported = 0

    for page_number in tqdm(
        range(start_page - 1, end_page),
        desc="Extracting"
    ):

        page = document.load_page(page_number)

        pix = page.get_pixmap(
            matrix=matrix,
            alpha=False
        )

        filename = (
            output_dir /
            f"Page_{page_number + 1:04d}.{image_format}"
        )

        pix.save(filename)

        exported += 1

    document.close()

    print("\nFinished.")
    print(f"Images Exported : {exported}")

    return exported


if __name__ == "__main__":

    pdf_to_images(
        pdf_path="input/book.pdf",
        output_dir="extracted",
        dpi=600,
        image_format="png"
    )
