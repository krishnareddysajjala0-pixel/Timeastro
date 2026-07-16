import math
from PIL import Image, ImageDraw, ImageFont

def draw_circular_text():
    base_img_path = r"C:\Users\gnana\.gemini\antigravity\brain\af2c4f22-2255-4448-87fd-e2f8d8b1cd3a\thraitha_logo_1784220073308.png"
    out_path = r"C:\Users\gnana\.gemini\antigravity\scratch\Timeastro\static\logo_with_text.png"
    
    base_img = Image.open(base_img_path).convert("RGBA")
    target_logo_size = 800
    base_img = base_img.resize((target_logo_size, target_logo_size), Image.Resampling.LANCZOS)
    
    font_size = 80
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\Nirmala.ttc", font_size)
    except:
        font = ImageFont.load_default()
        
    # The text is "త్రైత సిద్ధాంత జ్యోతిష్యం"
    # We manually split it into grapheme clusters to keep ligatures intact
    chars = ["త్రై", "త", " ", "సి", "ద్ధాం", "త", " ", "జ్యో", "తి", "ష్యం"]
    
    # We want to draw this along the top arc, or a full circle.
    # Let's space them out along an arc.
    padding = 150
    final_size = target_logo_size + padding * 2
    
    final_img = Image.new("RGBA", (final_size, final_size), (0, 0, 0, 0))
    
    # Paste base logo in the center
    final_img.paste(base_img, (padding, padding), base_img)
    
    # Radius for the text baseline
    radius = (target_logo_size / 2) + 50
    center = (final_size / 2, final_size / 2)
    
    # Calculate total angle needed for the text
    # We'll measure each character's width and map it to an angle
    dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1,1)))
    char_angles = []
    total_angle = 0
    
    for char in chars:
        bbox = dummy_draw.textbbox((0, 0), char, font=font)
        w = bbox[2] - bbox[0]
        # arc length = w. angle = w / radius
        angle = w / radius
        char_angles.append(angle)
        total_angle += angle
        
    # Add some spacing between characters
    spacing_angle = 15 / radius
    total_angle += spacing_angle * (len(chars) - 1)
    
    # Start angle so the text is centered at the top (-pi/2)
    start_angle = -math.pi/2 - (total_angle / 2)
    
    current_angle = start_angle
    
    # Create a separate layer to draw all text, then we can combine it
    text_layer = Image.new("RGBA", (final_size, final_size), (0, 0, 0, 0))
    
    for i, char in enumerate(chars):
        # We want the character's bottom center to be at the calculated point on the circle
        bbox = dummy_draw.textbbox((0, 0), char, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        
        char_angle = current_angle + (char_angles[i] / 2)
        
        # Position on the circle (using standard polar to cartesian)
        # For drawing at the top, angle is around -pi/2
        x = center[0] + radius * math.cos(char_angle)
        y = center[1] + radius * math.sin(char_angle)
        
        # Draw the character on a small temporary image, rotate it, and paste it
        temp_size = max(w, h) * 2
        temp_img = Image.new("RGBA", (temp_size, temp_size), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        
        # Draw exactly in the middle
        temp_draw.text((temp_size/2 - w/2, temp_size/2 - h/2), char, font=font, fill=(255, 215, 0, 255))
        
        # Rotate the character so it's tangential to the circle.
        # A tangent at angle 'char_angle' has angle 'char_angle + pi/2'.
        # Pillow rotation is counter-clockwise and in degrees.
        rot_degrees = -math.degrees(char_angle + math.pi/2)
        temp_rotated = temp_img.rotate(rot_degrees, resample=Image.Resampling.BICUBIC, expand=True)
        
        # Paste it onto the text layer
        # The center of temp_rotated should be at (x, y)
        paste_x = int(x - temp_rotated.width / 2)
        paste_y = int(y - temp_rotated.height / 2)
        
        text_layer.paste(temp_rotated, (paste_x, paste_y), temp_rotated)
        
        current_angle += char_angles[i] + spacing_angle
        
    final_img = Image.alpha_composite(final_img, text_layer)
    final_img.save(out_path)
    print("Done")

if __name__ == "__main__":
    draw_circular_text()
