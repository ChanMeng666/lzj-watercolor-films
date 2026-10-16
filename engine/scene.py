"""場景 = 若干按景深分開的水彩圖層 + 精靈 + 元數據；輸出 WebP 與 manifest.json"""
import os, json
import numpy as np
from wc import Layer, Paper, save_layer, save_gray, blur, F32

W, H = 2304, 1296          # 1.2 倍超採樣邊距，供視差鏡頭
_papers = {}


def paper_for(w, h, seed=7):
    k = (w, h, seed)
    if k not in _papers:
        _papers[k] = Paper(w, h, seed)
    return _papers[k]


class Scene:
    def __init__(self, film, name, seed=1, w=W, h=H):
        self.film, self.name = film, name
        self.w, self.h = w, h
        self.rng = np.random.default_rng(seed)
        self.paper = paper_for(w, h)
        self.layers = []   # (name, depth, Layer, opaque)
        self.sprites = []  # (name, Layer, anchor)
        self.tmaps = {}
        self.meta = {}

    def layer(self, name, depth, opaque=False):
        L = Layer(self.w, self.h, self.paper, np.random.default_rng(self.rng.integers(1 << 30)))
        self.layers.append((name, depth, L, opaque))
        return L

    def sprite(self, name, w, h, anchor=(0.5, 1.0)):
        p = paper_for(w, h, seed=11)
        L = Layer(w, h, p, np.random.default_rng(self.rng.integers(1 << 30)))
        self.sprites.append((name, L, anchor))
        return L

    def tmap(self, layer_name):
        t = np.full((self.h, self.w), 9.0, F32)
        self.tmaps[layer_name] = t
        return t

    def save(self, root):
        d = os.path.join(root, self.film, self.name)
        os.makedirs(d, exist_ok=True)
        man = {"name": self.name, "w": self.w, "h": self.h, "layers": [], "sprites": [], "meta": self.meta}
        for name, depth, L, opaque in self.layers:
            rgb, a = L.to_rgba(opaque)
            f = f"{name}.jpg" if opaque else f"{name}.webp"
            save_layer(os.path.join(d, f), rgb, None if opaque else a)
            ent = {"name": name, "file": f, "depth": depth}
            if name in self.tmaps:
                t = self.tmaps[name]
                # 未寫入處 (9) → 1；其餘歸一化到 0..0.98；並向外擴一點以免邊緣漏顯
                mx = t[t < 8].max() if (t < 8).any() else 1
                tt = np.where(t > 8, 1.0, np.clip(t / (mx if mx > 1 else 1), 0, 0.98))
                import cv2
                tt = cv2.erode(tt.astype(F32), np.ones((5, 5), np.uint8))
                save_gray(os.path.join(d, f"{name}_t.png"), tt)
                ent["tmap"] = f"{name}_t.png"
            man["layers"].append(ent)
        for name, L, anchor in self.sprites:
            rgb, a = L.to_rgba(False)
            f = f"sp_{name}.webp"
            save_layer(os.path.join(d, f), rgb, a)
            man["sprites"].append({"name": name, "file": f, "w": L.w, "h": L.h, "anchor": anchor})
        with open(os.path.join(d, "manifest.json"), "w", encoding="utf-8") as fp:
            json.dump(man, fp, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else (o.tolist() if hasattr(o, "tolist") else str(o)))

    def preview(self, path, scale=0.5):
        """白紙上平攤所有圖層（不含精靈）"""
        import cv2
        C = np.ones((self.h, self.w, 3), F32)
        for name, depth, L, opaque in self.layers:
            rgb, a = L.to_rgba(opaque)
            C = C * (1 - a[..., None]) + rgb * a[..., None]
        C = C * self.paper.texture_rgb()
        img = (np.clip(C[..., ::-1], 0, 1) * 255).astype(np.uint8)
        img = cv2.resize(img, (int(self.w * scale), int(self.h * scale)), interpolation=cv2.INTER_AREA)
        cv2.imwrite(path, img, [cv2.IMWRITE_JPEG_QUALITY, 88])
