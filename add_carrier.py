"""Create the canonical Trading Carrier version of each full-size pal PNG.

Each pal remains the full output canvas. `Trading_Carrier.png` is resized to
fit in the pal image's bottom-right quarter.

Requires Pillow:
    py -m pip install Pillow
"""

from pathlib import Path

from PIL import Image


FOLDER = Path(__file__).resolve().parent
CARRIER_NAME = "Trading_Carrier.png"
OUTPUT_SUFFIX = "_Carrier"
SMALL_SUFFIX = "Small"


def overlay_size_for(image_size: tuple[int, int], overlay_size: tuple[int, int]) -> tuple[int, int]:
    """Return the largest overlay size that fits in one image quadrant."""
    image_width, image_height = image_size
    overlay_width, overlay_height = overlay_size
    max_width = image_width // 2
    max_height = image_height // 2
    scale = min(max_width / overlay_width, max_height / overlay_height)
    return max(1, round(overlay_width * scale)), max(1, round(overlay_height * scale))


def is_full_size_pal(image_path: Path) -> bool:
    """Return whether a PNG is a source pal rather than a generated output."""
    return (
        image_path.name != CARRIER_NAME
        and not image_path.stem.endswith(SMALL_SUFFIX)
        and not image_path.stem.endswith(OUTPUT_SUFFIX)
    )


def main() -> None:
    carrier_path = FOLDER / CARRIER_NAME
    if not carrier_path.is_file():
        raise FileNotFoundError(f"Put '{CARRIER_NAME}' in {FOLDER} before running this script.")

    with Image.open(carrier_path) as source:
        carrier = source.convert("RGBA")

    for image_path in sorted(FOLDER.glob("*.png")):
        # Only full-size source pals receive a carrier.  Small files and
        # carrier files are generated outputs, so this remains idempotent and
        # never creates names such as FooSmall_Carrier.png.
        if not is_full_size_pal(image_path):
            continue

        output_path = image_path.with_name(f"{image_path.stem}{OUTPUT_SUFFIX}.png")
        with Image.open(image_path) as source:
            pal_background = source.convert("RGBA")

        resized_carrier = carrier.resize(
            overlay_size_for(pal_background.size, carrier.size), Image.Resampling.LANCZOS
        )
        # Anchor the carrier at the canvas's bottom-right corner.
        position = (
            pal_background.width - resized_carrier.width,
            pal_background.height - resized_carrier.height,
        )
        pal_background.alpha_composite(resized_carrier, dest=position)
        pal_background.save(output_path, "PNG")
        print(f"Created {output_path.name}")


if __name__ == "__main__":
    main()
