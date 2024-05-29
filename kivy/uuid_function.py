import uuid
from PIL import Image as PILImage
import piexif

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
    return unique_id




# def retrieve_uuid(image_path):
#     # Load the image
#     img = PILImage.open(image_path)
#     exif_data = piexif.load(img.info['exif'])

#     # Retrieve the UUID from the UserComment field
#     user_comment = exif_data['Exif'][piexif.ExifIFD.UserComment]
#     unique_id = user_comment.decode('utf-8')
#     img.close()
#     return unique_id

def retrieve_uuid(image_path):
    # Load the image
    img = PILImage.open(image_path)

    # Check if 'exif' data is present in the image
    if 'exif' in img.info:
        exif_data = piexif.load(img.info['exif'])

        # Retrieve the UUID from the UserComment field if it exists
        if piexif.ExifIFD.UserComment in exif_data['Exif']:
            user_comment = exif_data['Exif'][piexif.ExifIFD.UserComment]
            unique_id = user_comment.decode('utf-8')
            img.close()
            print(unique_id)
            return unique_id
        else:
            img.close()
            return "No UUID found in EXIF UserComment."
    else:
        img.close()
        return "No EXIF data found in image."