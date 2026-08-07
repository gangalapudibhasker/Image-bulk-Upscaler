"""
model_selector.py
Professional AI Book Image Enhancement Suite

Phase 2 - Step 11

AI Model Selection Engine

Author : Gangalapudi Bhasker Project
Version : 1.0
"""

from dataclasses import dataclass


@dataclass
class ModelSelection:

    model: str

    scale: int

    enhancement_mode: str

    reason: str


class ModelSelector:

    def __init__(self):

        self.models = {

            "geometry":
            {
                "model": "RealESRGAN_x4plus_anime_6B",
                "scale": 4,
                "mode": "line_art"
            },

            "graph":
            {
                "model": "RealESRGAN_x4plus",
                "scale": 4,
                "mode": "graph"
            },

            "photo":
            {
                "model": "SwinIR",
                "scale": 4,
                "mode": "photo"
            },

            "illustration":
            {
                "model": "BSRGAN",
                "scale": 4,
                "mode": "illustration"
            },

            "cartoon":
            {
                "model": "RealESRGAN_x4plus_anime_6B",
                "scale": 4,
                "mode": "cartoon"
            },

            "table":
            {
                "model": "RealESRGAN_x4plus",
                "scale": 2,
                "mode": "text_preserve"
            },

            "mixed":
            {
                "model": "Hybrid",
                "scale": 4,
                "mode": "hybrid"
            },

            "unknown":
            {
                "model": "RealESRGAN_x4plus",
                "scale": 4,
                "mode": "default"
            }
        }

    # --------------------------------------------------

    def select(
        self,
        image_type
    ):

        image_type = image_type.lower()

        if image_type not in self.models:

            image_type = "unknown"

        cfg = self.models[image_type]

        return ModelSelection(

            model=cfg["model"],

            scale=cfg["scale"],

            enhancement_mode=cfg["mode"],

            reason=f"Selected because image type = {image_type}"

        )

    # --------------------------------------------------

    def print_available_models(self):

        print()

        print("=" * 60)

        print("AVAILABLE MODELS")

        print("=" * 60)

        for key, value in self.models.items():

            print(

                f"{key:15s}"

                f"{value['model']:30s}"

                f"{value['scale']}x"

            )


# ------------------------------------------------------

if __name__ == "__main__":

    selector = ModelSelector()

    selector.print_available_models()

    print()

    print(

        selector.select("geometry")

    )

    print(

        selector.select("graph")

    )

    print(

        selector.select("photo")

    )
