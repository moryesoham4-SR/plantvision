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

def validate_leaf_image(image_input) -> tuple[bool, str, dict]:
    """
    Strict agricultural validation for crop leaves (Potato, Tomato).
    Rejects human faces, selfies, furniture, curtains, and non-plant objects.
    """
    try:
        if not isinstance(image_input, Image.Image):
            img = Image.open(image_input)
        else:
            img = image_input

        if img.mode != "RGB":
            img_rgb = img.convert("RGB")
        else:
            img_rgb = img

        # Downsample for fast pixel-level metric analysis
        small_img = img_rgb.resize((150, 150))
        arr = np.array(small_img, dtype=np.float32)

        R = arr[:, :, 0]
        G = arr[:, :, 1]
        B = arr[:, :, 2]

        # 1. Excess Green Index (ExG = 2*G - R - B)
        exg = 2 * G - R - B
        
        # 2. HSV Green & Plant Foliage Hue Range
        hsv = small_img.convert("HSV")
        h, s, v = hsv.split()
        h_arr = np.array(h, dtype=np.float32)
        s_arr = np.array(s, dtype=np.float32)
        v_arr = np.array(v, dtype=np.float32)

        # In PIL HSV: Green/Yellow-Green hue is 22 to 105 (equivalent to 32° to 150°)
        green_foliage_mask = (
            (h_arr >= 22) & (h_arr <= 105) & 
            (s_arr >= 25) & (v_arr >= 25) &
            (G >= R * 0.95) & (G >= B * 1.05)
        )
        green_ratio = float(np.sum(green_foliage_mask) / (150 * 150))

        # 3. Detect Human Skin / Face
        skin_mask = (
            (R > 85) & (G > 35) & (B > 20) &
            ((R - G) > 12) & (R > B) & ((R - B) > 12) & 
            (G >= B * 0.8) &
            (h_arr < 22)  # Red/Orange human hue range
        )
        skin_ratio = float(np.sum(skin_mask) / (150 * 150))

        # Real leaves MUST have at least 15% green vegetative chlorophyll area
        if green_ratio < 0.15:
            if skin_ratio > 0.25:
                return False, "⚠️ Human face or selfie detected! Please do not point the camera at people. Aim the camera directly at a real Potato or Tomato plant leaf.", {
                    "green_ratio": green_ratio,
                    "skin_ratio": skin_ratio
                }
            else:
                return False, f"⚠️ Non-plant object detected! Real agricultural foliage was not found (detected plant color: {green_ratio*100:.1f}%). Please position a real crop leaf in front of the camera.", {
                    "green_ratio": green_ratio,
                    "skin_ratio": skin_ratio
                }

        # If skin tone dominates over green foliage
        if skin_ratio > 0.40 and green_ratio < 0.30:
            return False, "⚠️ Human subject detected. Please focus exclusively on the crop leaf blade.", {
                "green_ratio": green_ratio,
                "skin_ratio": skin_ratio
            }

        return True, "🌿 Valid crop leaf verified.", {
            "green_ratio": green_ratio,
            "skin_ratio": skin_ratio
        }
    except Exception as e:
        return True, f"Validation fallback: {e}", {"green_ratio": 1.0, "skin_ratio": 0.0}



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


