import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

def create_circular_logo(image_path, text, out_path):
    # 1. Load base logo and resize if needed
    base_img = Image.open(image_path).convert("RGBA")
    
    # Target size for the logo
    target_logo_size = 800
    base_img = base_img.resize((target_logo_size, target_logo_size), Image.Resampling.LANCZOS)
    
    # 2. We want the text to wrap around in a circle.
    # Pillow handles basic Telugu shaping via HarfBuzz if installed, but windows usually works okay with Nirmala.
    font_size = 64
    try:
        font = ImageFont.truetype("Nirmala.ttf", font_size)
    except:
        font = ImageFont.load_default()
        
    # Create a large transparent image for the text
    # The circumference should be slightly larger than the text length to wrap around
    dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1,1)))
    bbox = dummy_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # The radius of the text circle
    # Circumference = 2 * pi * r => r = Circumference / (2 * pi)
    # Let's add some padding to text_width so it doesn't touch itself
    circumference = max(text_width + 200, target_logo_size * 3.14159 + 200)
    radius = circumference / (2 * math.pi)
    
    # Now we need to place characters along the circle.
    # Because of ligatures, we can't easily split by char.
    # Instead, let's just write the text to a wide transparent image, and use OpenCV to warp polar!
    
    # To use warpPolar, the image should be rectangular.
    # Width = Circumference, Height = radius + text_height
    wrap_width = int(circumference)
    wrap_height = int(radius + text_height * 2)
    
    text_img = Image.new("RGBA", (wrap_width, wrap_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_img)
    
    # Draw text in the middle horizontally, at the bottom of the image (which maps to the outer edge of the polar warp)
    x_pos = (wrap_width - text_width) // 2
    y_pos = wrap_height - text_height - 20
    draw.text((x_pos, y_pos), text, font=font, fill=(255, 215, 0, 255)) # Gold text
    
    # Convert to OpenCV format
    text_cv = np.array(text_img)
    
    # Warp Polar!
    # Flags: WARP_INVERSE_MAP + INTER_LINEAR
    # warpPolar maps (rho, phi) to (x, y)
    center = (wrap_height, wrap_height)
    max_radius = wrap_height
    
    # We want the linear image to wrap into a circle.
    # linearPolar converts cartesian to polar or vice versa.
    # cv2.WARP_INVERSE_MAP means we map polar TO cartesian.
    flags = cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR | cv2.WARP_FILL_OUTLIERS
    
    warped_cv = cv2.warpPolar(text_cv, (wrap_height*2, wrap_height*2), center, max_radius, flags)
    
    # Convert back to PIL
    warped_pil = Image.fromarray(warped_cv, "RGBA")
    
    # Paste base logo into the center of the warped text image
    final_size = wrap_height * 2
    final_img = Image.new("RGBA", (final_size, final_size), (0, 0, 0, 0))
    final_img.paste(warped_pil, (0, 0), warped_pil)
    
    # Center paste base logo
    offset_x = (final_size - target_logo_size) // 2
    offset_y = (final_size - target_logo_size) // 2
    final_img.paste(base_img, (offset_x, offset_y), base_img)
    
    final_img.save(out_path)
    print("Saved logo to", out_path)

if __name__ == "__main__":
    create_circular_logo(
        r"C:\Users\gnana\.gemini\antigravity\brain\af2c4f22-2255-4448-87fd-e2f8d8b1cd3a\thraitha_logo_1784220073308.png",
        "త్రైత సిద్ధాంత జ్యోతిష్యం",
        r"C:\Users\gnana\.gemini\antigravity\scratch\Timeastro\static\logo_with_text.png"
    )
