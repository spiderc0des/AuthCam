# from kivy.app import App
# from kivy.uix.camera import Camera
# from kivy.uix.boxlayout import BoxLayout

# class TestCameraApp(App):
#     def build(self):
#         layout = BoxLayout()
#         self.camera = Camera(play=True)
#         self.camera.resolution = (640, 480)  # Adjust to your camera's supported resolution
#         layout.add_widget(self.camera)
#         return layout

# if __name__ == '__main__':
#     TestCameraApp().run()

from PIL import Image as PILImage
import hashlib
import io
import uuid
import piexif

def hash_image():

    image_path = input('enter image path: ')

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


# hash_image()

def add_uuid(image_path):
 # Generate a unique identifier
    unique_id = str(uuid.uuid4())

     # Load the image using PIL
    image = PILImage.open(image_path)

    # Add the UUID to the EXIF data
    exif_dict = {'Exif': {piexif.ExifIFD.UserComment: unique_id.encode('utf-8')}}
    exif_bytes = piexif.dump(exif_dict)
    image.save(image_path, "png", exif=exif_bytes)
    print(f"Image saved with UUID: {unique_id}")

    return image_path

add_uuid('captured.png')


def retrieve_uuid(image_path):
    # Load the image
    img = PILImage.open(image_path)
    exif_data = piexif.load(img.info['exif'])

    # Retrieve the UUID from the UserComment field
    user_comment = exif_data['Exif'][piexif.ExifIFD.UserComment]
    unique_id = user_comment.decode('utf-8')
    img.close()

    print(f"UUID retrieved from image: {unique_id}")
    return unique_id

retrieve_uuid('captured.png')
