from PIL import Image
import numpy as np

def analyze_color(path, name):
    try:
        img = Image.open(path).convert("HSV")
    except Exception as e:
        print(f"Failed to load {path}: {e}")
        return
    arr = np.array(img)
    h, s, v = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    
    # 排除純背景（v > 200 且 s < 35 的接近灰白背景）
    fg_mask = (s > 30) & (v < 245)
    fg_s = s[fg_mask]
    fg_v = v[fg_mask]
    
    mean_s = np.mean(fg_s) if len(fg_s) > 0 else 0
    max_s = np.max(fg_s) if len(fg_s) > 0 else 0
    mean_v = np.mean(fg_v) if len(fg_v) > 0 else 0
    
    print(f"[{name:22s}] 前景平均飽和度: {mean_s/255*100:4.1f}% | 最高飽和度: {max_s/255*100:4.1f}% | 明度: {mean_v/255*100:4.1f}%")

print("=== 原始參考片色彩 ===")
analyze_color(r"c:\antigravity\影片\逆向研究\claude3d_工法\ref_slice_03s.jpg", "Ref 03s (Book)")
analyze_color(r"c:\antigravity\影片\逆向研究\claude3d_工法\ref_slice_22s.jpg", "Ref 22s (Spring Box)")
analyze_color(r"c:\antigravity\影片\逆向研究\claude3d_工法\ref_slice_45s.jpg", "Ref 45s (Bookshelf)")

print("\n=== 我們目前的影片色彩 ===")
analyze_color(r"c:\antigravity\影片\逆向研究\claude3d_工法\mp4_verify_01.jpg", "Ours S1 (Box)")
analyze_color(r"c:\antigravity\影片\逆向研究\claude3d_工法\final_check_s2.jpg", "Ours S2 (Binder)")
analyze_color(r"c:\antigravity\影片\逆向研究\claude3d_工法\final_check_s4.jpg", "Ours S4 (Podium)")
