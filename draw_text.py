import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

def create_circular_logo(image_path, text, out_path):
    base_img = Image.open(image_path).convert("RGBA")
    target_logo_size = 800
    base_img = base_img.resize((target_logo_size, target_logo_size), Image.Resampling.LANCZOS)
    
    font_size = 80
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\Nirmala.ttc", font_size)
    except:
        font = ImageFont.load_default()
        
    dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1,1)))
    bbox = dummy_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # We want text around the outer edge.
    padding_around_logo = 100
    radius = (target_logo_size / 2) + padding_around_logo
    
    # In OpenCV polar mapping:
    # y-axis corresponds to angle (0 to 360)
    # x-axis corresponds to radius (0 to max_radius)
    # Max radius for the output image
    max_radius = int(radius + text_height + 50)
    
    # Circumference determines how much the text stretches along the circle.
    # In OpenCV, y goes from 0 to output_size. 
    # Let's make the polar image have height = int(2 * pi * max_radius)
    circumference = int(2 * math.pi * max_radius)
    
    polar_img = Image.new("RGBA", (max_radius, circumference), (0, 0, 0, 0))
    polar_draw = ImageDraw.Draw(polar_img)
    
    # Draw text. We want it along the y-axis, but PIL draws horizontally.
    # So we draw it horizontally on a temporary image and rotate it 90 degrees.
    temp_img = Image.new("RGBA", (circumference, max_radius), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Center text horizontally, place at the bottom (which maps to outer radius)
    x_pos = (circumference - text_width) // 2
    # Place text so it is at distance 'radius' from the top
    y_pos = int(radius)
    temp_draw.text((x_pos, y_pos), text, font=font, fill=(255, 215, 0, 255))
    
    # OpenCV maps angle 0 to top, sweeping clockwise (depending on flags).
    # Rotate the image so X becomes Y.
    polar_img = temp_img.transpose(Image.TRANSPOSE)
    
    # Convert to OpenCV format
    polar_cv = np.array(polar_img)
    
    # Warp Polar!
    final_size = max_radius * 2
    center = (final_size // 2, final_size // 2)
    
    flags = cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR | cv2.WARP_FILL_OUTLIERS
    warped_cv = cv2.warpPolar(polar_cv, (final_size, final_size), center, max_radius, flags)
    
    warped_pil = Image.fromarray(warped_cv, "RGBA")
    
    # Paste base logo into the center of the warped text image
    final_img = Image.new("RGBA", (final_size, final_size), (0, 0, 0, 0))
    final_img.paste(warped_pil, (0, 0), warped_pil)
    
    offset_x = (final_size - target_logo_size) // 2
    offset_y = (final_size - target_logo_size) // 2
    final_img.paste(base_img, (offset_x, offset_y), base_img)
    
    # Save a debug image to see if text rendered
    temp_img.save("debug_temp.png")
    
    final_img.save(out_path)
    print("Saved logo to", out_path)

if __name__ == "__main__":
    create_circular_logo(
        r"C:\Users\gnana\.gemini\antigravity\brain\af2c4f22-2255-4448-87fd-e2f8d8b1cd3a\thraitha_logo_1784220073308.png",
        "త్రైత సిద్ధాంత జ్యోతిష్యం",
        r"C:\Users\gnana\.gemini\antigravity\scratch\Timeastro\static\logo_with_text.png"
    )
