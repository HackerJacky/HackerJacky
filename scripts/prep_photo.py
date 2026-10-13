import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def prep(input_path, output_path="source-prepped.png"):
    img = Image.open(input_path)
    nobg = remove(img)  # 自動去背
    
    # 轉為純白背景
    canvas = Image.new("RGBA", nobg.size, (255, 255, 255, 255))
    canvas.paste(nobg, (0, 0), nobg)
    gray = cv2.cvtColor(np.array(canvas.convert("RGB")), cv2.COLOR_RGB2GRAY)
    
    # CLAHE 對比強化，確保臉部輪廓清晰
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    cv2.imwrite(output_path, enhanced)
    print(f"Prepped photo saved to {output_path}")

if __name__ == "__main__":
    prep(sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg")