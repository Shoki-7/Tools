import os
import re
from PIL import Image, ImageDraw, ImageFont
from natsort import natsorted

def pngs_to_gif(folder_path, duration=200, bg_color=(255, 255, 255), is_time_show = False, is_field_show = False, time_step = 1e-11):
    png_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".png")]
    png_files = natsorted(png_files)
    if not png_files:
        print("PNGファイルが見つかりません。")
        return

    frames = []
    for filename in png_files:
        filepath = os.path.join(folder_path, filename)
        img = Image.open(filepath).convert("RGBA")
        
        # 透過背景を白で塗りつぶす
        bg = Image.new("RGBA", img.size, bg_color + (255,))
        img = Image.alpha_composite(bg, img)

        if is_time_show:
            # 正規表現で regtXXXXtoYYYY を抽出
            match = re.search(r"regt(\d{4})to(\d{4})", filename)
            if match:
                start = int(match.group(1))
                end = int(match.group(2))
                t_center = (start + end) // 2
                t_label = f"t = {t_center * time_step * 1e9:.1f} ns"
            else:
                t_label = "t = ?"

        if is_field_show:
            # 正規表現で regtXXXXtoYYYY を抽出
            match = re.search(r"Hext([0-9]+(?:\.[0-9]+)?)mT", filename)
            if match:
                start = float(match.group(1))
                t_label = f"μ0Hext = {start:.1f} mT"
                t_label = f"         {start:.1f} mT"
            else:
                t_label = "μ0Hext = ?"

        if is_time_show or is_field_show:
            # テキストを画像に描画
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 50)
            except:
                font = ImageFont.load_default()
            draw.text((190, 950), t_label, font=font, fill=(255, 255, 255))

        frames.append(img.convert("RGB"))

    # 出力先パス
    parent_folder = os.path.dirname(folder_path.rstrip(os.sep))
    output_path = os.path.join(parent_folder, "animation.gif")

    # GIF保存
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )
    print(f"GIFを出力しました: {output_path}")

input_dir = input("Dir: ")

is_time_show = True
is_field_show = False
time_step = 2e-11   # s
pngs_to_gif(input_dir, duration=400, is_time_show=is_time_show, is_field_show=is_field_show, time_step=time_step)
