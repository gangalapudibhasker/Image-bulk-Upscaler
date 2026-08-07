"""
upscale.py
Professional AI Book Image Enhancement Suite

Phase 1 - Step 3
Batch AI Image Upscaler

Author : Gangalapudi Bhasker Project
"""

from pathlib import Path
import subprocess
from tqdm import tqdm


SUPPORTED = (
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
)


def batch_upscale(
    input_dir,
    output_dir,
    model="RealESRGAN_x4plus",
    scale=4,
    skip_existing=True,
):

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    images = []

    for ext in SUPPORTED:
        images.extend(input_dir.glob(f"*{ext}"))

    images = sorted(images)

    print("=" * 60)
    print("AI BATCH UPSCALER")
    print("=" * 60)
    print(f"Images : {len(images)}")
    print(f"Model  : {model}")
    print(f"Scale  : {scale}x")
    print("=" * 60)

    failed = []

    for image in tqdm(images):

        output_file = output_dir / image.name

        if skip_existing and output_file.exists():
            continue

        cmd = [
            "python",
            "inference_realesrgan.py",
            "-n",
            model,
            "-i",
            str(image),
            "-o",
            str(output_dir),
            "-s",
            str(scale),
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            failed.append(image.name)

    print()

    print("Completed.")

    if failed:

        print()

        print("Failed Images")

        for f in failed:
            print(f)

    return failed


if __name__ == "__main__":

    batch_upscale(
        input_dir="extracted",
        output_dir="enhanced",
        model="RealESRGAN_x4plus",
        scale=4,
    )
