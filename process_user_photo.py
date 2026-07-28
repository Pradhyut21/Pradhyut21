import os
from PIL import Image, ImageEnhance

img_path = r"C:\Users\maruthi Prasad\.gemini\antigravity-ide\brain\32abb352-af82-45e2-b7a6-fca0db3a3ef7\media__1785232102743.png"

ASCII_CHARS = "@%#*+=-:. " # Contrast mapped chars

def photo_to_ascii(path, width=41, height=26):
    img = Image.open(path).convert('L')
    # Enhance contrast slightly for crisp ASCII art
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.4)
    
    # Crop around head and upper body
    w, h = img.size
    crop_box = (int(w * 0.15), int(h * 0.05), int(w * 0.85), int(h * 0.82))
    img = img.crop(crop_box)
    
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    pixels = img.getdata()
    lines = []
    current_line = ""
    for i, p in enumerate(pixels):
        char_idx = int(p / 256 * len(ASCII_CHARS))
        current_line += ASCII_CHARS[char_idx]
        if (i + 1) % width == 0:
            lines.append(current_line)
            current_line = ""
    return lines

lines = photo_to_ascii(img_path)

# Build SVG tspan lines
y_start = 70
y_step = 13
tspans = []
for i, line in enumerate(lines):
    y = y_start + i * y_step
    # Escape special XML chars if any
    line_xml = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    tspans.append(f'          <tspan x="20" y="{y}">{line_xml}</tspan>')

ascii_block = "\n".join(tspans)
print("ASCII Block generated:")
print(ascii_block)

with open("ascii_exact.txt", "w", encoding="utf-8") as f:
    f.write(ascii_block)
