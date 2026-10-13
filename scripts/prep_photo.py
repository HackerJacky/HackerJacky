import sys
import cv2
import numpy as np
from PIL import Image
from rembg import new_session, remove

def prep(input_path, output_path="source-prepped.png"):
    img = Image.open(input_path).convert("RGB")
    # u2netp 是輕量版模型（約 5MB），人像去背夠用；想要更精細可改成 "u2net"（約 170MB）
    nobg = remove(img, session=new_session("u2netp"))  # 自動去背（RGBA，背景 alpha=0）
    rgba = np.array(nobg)
    alpha = rgba[:, :, 3]

    # 只保留最大的一塊前景（人物），去掉門把、窗框之類的零碎殘留
    n, labels, stats, _ = cv2.connectedComponentsWithStats((alpha > 127).astype(np.uint8))
    if n > 1:
        biggest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        alpha = np.where(labels == biggest, alpha, 0).astype(np.uint8)
    gray = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2GRAY)

    # CLAHE 對比強化，確保臉部輪廓清晰
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # 存成「灰階 + 透明度」，讓 make_ascii_svg.py 用透明度判斷哪裡是背景
    Image.fromarray(np.dstack([enhanced, alpha]), "LA").save(output_path)
    print(f"Prepped photo saved to {output_path}")

if __name__ == "__main__":
    prep(sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg")
