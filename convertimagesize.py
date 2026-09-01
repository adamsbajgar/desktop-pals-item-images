"""Create or replace 200x200 `Small` PNG versions of the source images.

Requires Pillow:
    py -m pip install Pillow
"""

from pathlib import Path

from PIL import Image


FOLDER = Path(__file__).resolve().parent
CARRIER_NAME = "Trading_Carrier.png"
VALID_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
SMALL_SUFFIX = "Small"


def main() -> None:
    for image_path in sorted(FOLDER.iterdir()):
        # Existing Small files and the carrier artwork are outputs/assets,
        # never pal sources. This prevents names such as FooSmallSmall.png
        # and Trading_CarrierSmall.png from being generated.
        if (
            not image_path.is_file()
            or image_path.suffix.lower() not in VALID_EXTENSIONS
            or image_path.name == CARRIER_NAME
            or image_path.stem.endswith(SMALL_SUFFIX)
        ):
            continue

        output_path = image_path.with_name(f"{image_path.stem}Small.png")
        try:
            with Image.open(image_path) as source:
                resized = source.resize((200, 200), Image.Resampling.LANCZOS)
                # PNG output preserves transparency when the source has it.
                if "A" in resized.getbands():
                    resized = resized.convert("RGBA")
                else:
                    resized = resized.convert("RGB")
                resized.save(output_path, "PNG")
            print(f"Created or replaced: {output_path.name}")
        except (OSError, ValueError) as error:
            print(f"Failed processing {image_path.name}: {error}")


if __name__ == "__main__":
    main()
