import hashlib
from PIL import Image as PILImage
import io

def hash_image(image_path):
    # Open the image and convert it to bytes
        with PILImage.open(image_path) as img:
            byte_arr = io.BytesIO()
            img.save(byte_arr, format='PNG')  # Save image to byte array
            image_bytes = byte_arr.getvalue()

        # Generate a hash for the image
        hash_obj = hashlib.sha256()
        hash_obj.update(image_bytes)
        image_hash = hash_obj.hexdigest()
        print(f'{image_path}')
        print(f"Hash of the captured image: {image_hash}")
        return image_hash