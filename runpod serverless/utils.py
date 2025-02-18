import base64
from io import BytesIO
from PIL import Image
from IPython.display import display

def display_image(image, max_size=100):
    max_size = (max_size, max_size)
    image_data = base64.b64decode(image)
    image = Image.open(BytesIO(image_data))
    # Resize the image while maintaining aspect ratio
    image.thumbnail(max_size)
    display(image)