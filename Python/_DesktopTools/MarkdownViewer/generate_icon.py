# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: generate_icon.py
# ☆ Description: Generates multi-resolution .ico asset for Galactic Markdown Editor
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from PIL import Image, ImageDraw

def create_galaxy_icon(output_path):
    sizes = [(256, 256), (48, 48), (32, 32), (16, 16)]
    images = []

    for width, height in sizes:
        # Create transparent base
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Scale factor relative to 256
        s = width / 256.0

        # Background rounded badge: Dark spaceship slate (#0f131a)
        pad = int(8 * s)
        corner_radius = int(48 * s)
        badge_box = [pad, pad, width - pad, height - pad]
        draw.rounded_rectangle(
            badge_box, 
            radius=corner_radius, 
            fill=(15, 19, 26, 255), 
            outline=(126, 231, 135, 255),  # Alien mint border
            width=max(1, int(10 * s))
        )

        # Draw a stylized Markdown 'M' and cosmic star in Alien Mint (#7ee787) and Star White (#e2e8f0)
        mint = (126, 231, 135, 255)
        white = (226, 240, 240, 255)
        
        # 'M' coordinates scaled
        m_x0 = int(55 * s)
        m_x1 = int(75 * s)
        m_x_mid = int(105 * s)
        m_x2 = int(135 * s)
        m_x3 = int(155 * s)
        m_y_top = int(80 * s)
        m_y_bot = int(175 * s)
        m_y_dip = int(135 * s)

        m_polygon = [
            (m_x0, m_y_top), (m_x1, m_y_top),
            (m_x_mid, m_y_dip),
            (m_x2, m_y_top), (m_x3, m_y_top),
            (m_x3, m_y_bot), (m_x2, m_y_bot),
            (m_x2, m_y_top + int(30 * s)),
            (m_x_mid, m_y_bot - int(15 * s)),
            (m_x1, m_y_top + int(30 * s)),
            (m_x1, m_y_bot), (m_x0, m_y_bot)
        ]
        draw.polygon(m_polygon, fill=mint)

        # Arrow
        arr_x = int(190 * s)
        arr_top = int(80 * s)
        arr_bot = int(145 * s)
        w_stem = max(1, int(10 * s))
        draw.rectangle([arr_x - w_stem // 2, arr_top, arr_x + w_stem // 2, arr_bot], fill=white)
        arr_head = [
            (arr_x - int(24 * s), arr_bot),
            (arr_x + int(24 * s), arr_bot),
            (arr_x, arr_bot + int(30 * s))
        ]
        draw.polygon(arr_head, fill=white)

        # Little cosmic star in the corner
        star_x = int(210 * s)
        star_y = int(50 * s)
        star_r = int(10 * s)
        if star_r >= 2:
            draw.line([(star_x - star_r, star_y), (star_x + star_r, star_y)], fill=mint, width=max(1, int(2 * s)))
            draw.line([(star_x, star_y - star_r), (star_x, star_y + star_r)], fill=mint, width=max(1, int(2 * s)))

        images.append(img)

    # Save as multi-resolution icon
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    images[0].save(
        output_path, 
        format="ICO", 
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )
    print(f"✨ Icon created successfully: {output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(current_dir, "assets")
    output_ico = os.path.join(assets_dir, "galaxy_md.ico")
    create_galaxy_icon(output_ico)
