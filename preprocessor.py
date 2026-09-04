import io
import base64
import numpy as np
from PIL import Image
import config

def image_to_base64(img: Image.Image, max_dim: int = 400, quality: int = 80) -> str:
    """Converts a PIL Image to an optimized Base64 JPEG data URL for permanent cloud storage."""
    try:
        thumb = img.copy()
        thumb.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        if thumb.mode != "RGB":
            thumb = thumb.convert("RGB")
        buffered = io.BytesIO()
        thumb.save(buffered, format="JPEG", quality=quality, optimize=True)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{img_str}"
    except Exception as e:
        print(f"Base64 conversion error: {e}")
        return ""

def preprocess_image(image_input) -> tuple[Image.Image, Image.Image, np.ndarray, dict]:
    """
    Standardizes input images to 224x224 RGB float32 arrays normalized to [0, 1].
    """
    if not isinstance(image_input, Image.Image):
        img = Image.open(image_input)
    else:
        img = image_input

    # Ensure RGB
    if img.mode != "RGB":
        img = img.convert("RGB")

    orig_width, orig_height = img.size

    # Resize to exact model resolution
    resized_img = img.resize(config.IMAGE_TARGET_SIZE, Image.Resampling.BILINEAR)

    # Convert to float32 NumPy array normalized to [0.0, 1.0]
    img_array = np.array(resized_img, dtype=np.float32) / 255.0

    # Expand batch dimension: shape (1, 224, 224, 3)
    tensor_input = np.expand_dims(img_array, axis=0)

    metadata = {
        "original_size": (orig_width, orig_height),
        "processed_size": config.IMAGE_TARGET_SIZE,
        "channels": config.IMAGE_CHANNELS,
        "tensor_shape": tensor_input.shape,
        "min_pixel_val": float(img_array.min()),
        "max_pixel_val": float(img_array.max())
    }

    return img, resized_img, tensor_input, metadata


