from PIL import Image
import os

# Get the folder where the script is located
folder_path = os.path.dirname(os.path.abspath(__file__))

# Go through all files in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # Skip directories
    if not os.path.isfile(file_path):
        continue

    # Supported image extensions
    valid_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

    if filename.lower().endswith(valid_extensions):
        try:
            # Open image
            img = Image.open(file_path)

            # Resize to 200x200
            resized = img.resize((200, 200), Image.LANCZOS)

            # Create new filename
            name, _ = os.path.splitext(filename)
            new_filename = f"{name}Small.png"
            new_path = os.path.join(folder_path, new_filename)

            # Save as PNG
            resized.save(new_path, "PNG")

            print(f"Created: {new_filename}")

        except Exception as e:
            print(f"Failed processing {filename}: {e}")

print("Done.")