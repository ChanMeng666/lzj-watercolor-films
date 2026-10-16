"""全片共用紋理：螢幕空間紙紋 paper.jpg、轉場噪聲 noise.png"""
import os, sys
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(__file__))
from wc import Paper, fbm
out = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web", "assets")
os.makedirs(out, exist_ok=True)
P = Paper(1920, 1080, seed=3)
cv2.imwrite(os.path.join(out, "paper.jpg"), (P.texture_rgb()[..., ::-1] * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 94])
rng = np.random.default_rng(5)
n1 = fbm(540, 960, 4, rng, 6, 0.55)
n2 = fbm(540, 960, 16, rng, 4, 0.5)
n3 = fbm(540, 960, 2, rng, 3, 0.5)
cv2.imwrite(os.path.join(out, "noise.png"), (np.dstack([n3, n2, n1]) * 255).astype(np.uint8))
print("ok")
