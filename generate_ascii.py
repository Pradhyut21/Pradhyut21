import os
import glob
from PIL import Image

def find_user_image():
    search_dirs = [
        r"C:\Users\maruthi Prasad\.gemini\antigravity-ide\brain",
        r"C:\Users\maruthi Prasad\.gemini\antigravity-ide",
        os.path.expanduser("~")
    ]
    found_files = []
    for d in search_dirs:
        for ext in ['*.jpg', '*.png', '*.webp', '*.jpeg']:
            found_files.extend(glob.glob(os.path.join(d, '**', ext), recursive=True))
    
    # Sort by modification time descending
    found_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return found_files

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def image_to_ascii(img_path, width=41, height=26):
    img = Image.open(img_path).convert('L')
    # Crop to portrait head/shoulders
    w, h = img.size
    # Center crop focus on head and upper body
    crop_box = (int(w * 0.15), int(h * 0.05), int(w * 0.85), int(h * 0.85))
    img = img.crop(crop_box)
    
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    pixels = img.getdata()
    ascii_str = ""
    for i, p in enumerate(pixels):
        ascii_str += ASCII_CHARS[int(p / 256 * len(ASCII_CHARS))]
        if (i + 1) % width == 0:
            ascii_str += "\n"
    return ascii_str

files = find_user_image()
print(f"Found {len(files)} image files.")
if files:
    print("Latest image:", files[0])
    try:
        art = image_to_ascii(files[0])
        print("--- GENERATED ASCII ---")
        print(art)
        with open("ascii_output.txt", "w", encoding="utf-8") as f:
            f.write(art)
    except Exception as e:
        print("Error processing image:", e)
