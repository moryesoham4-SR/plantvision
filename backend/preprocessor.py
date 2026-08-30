import io
import numpy as np
from PIL import Image
from config import IMAGE_SIZE

def preprocess_image(image_input):
    "
    Takes an uploaded file, byte stream, or PIL Image,
    converts to RGB, resizes to exactly 224x224x3,
    and returns both the displayable PIL Image and normalized NumPy array.
    "
    if isinstance(image_input, (bytes, bytearray)):
        image = Image.open(io.BytesIO(image_input))
    elif hasattr(image_input, read):
        # UploadedFile / BytesIO
        image_input.seek(0)
        image = Image.open(image_input)
    elif isinstance(image_input, Image.Image):
        image = image_input
    else:
        raise ValueError(Unsupported image input type.)

    # 1. Convert to RGB (handles RGBA, Grayscale, etc.)
    if image.mode != RGB:
        image = image.convert(RGB)

    # 2. Resize to exact target dimensions (224 x 224)
    display_image = image.copy()
    resized_image = image.resize(IMAGE_SIZE, Image.Resampling.BILINEAR)

    # 3. Convert to NumPy array with shape (224, 224, 3)
    img_array = np.array(resized_image, dtype=np.float32)

    # 4. Normalize pixel values to [0.0, 1.0]
    normalized_array = img_array / 255.0

    # 5. Expand batch dimensions -> (1, 224, 224, 3)
    tensor_input = np.expand_dims(normalized_array, axis=0)

    metadata = {
        original_size: display_image.size,
        processed_size: IMAGE_SIZE,
        channels: 3,
        dtype: str(tensor_input.dtype),
        tensor_shape: tensor_input.shape
    }

    return display_image, resized_image, tensor_input, metadata
