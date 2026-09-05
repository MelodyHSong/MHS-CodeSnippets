# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: generate_icon.py
# ☆ Description: Generates multi-resolution .ico asset for StellarNotes
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import sys
import math

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from PIL import Image, ImageDraw

def draw_star(draw, cx, cy, r_outer, r_inner, points=5, fill=(242, 204, 96, 255), outline=None, width=1):
    """Draws a star polygon given center, outer radius, and inner radius."""
    poly = []
    angle_step = math.pi / points
    # Start pointing up (-pi/2)
    start_angle = -math.pi / 2
    for i in range(2 * points):
        r = r_outer if i % 2 == 0 else r_inner
        ang = start_angle + i * angle_step
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        poly.append((x, y))
    draw.polygon(poly, fill=fill, outline=outline, width=width)

def create_stellar_icon(output_path):
    sizes = [(256, 256), (48, 48), (32, 32), (16, 16)]
    images = []

    for width, height in sizes:
        # Create transparent base
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Scale factor relative to 256
        s = width / 256.0

        # Background rounded badge: Dark space slate (#0d1117)
        pad = int(8 * s)
        corner_radius = int(44 * s)
        badge_box = [pad, pad, width - pad, height - pad]
        draw.rounded_rectangle(
            badge_box, 
            radius=corner_radius, 
            fill=(13, 17, 23, 255), 
            outline=(227, 179, 65, 255),  # Stellar Gold border
            width=max(1, int(9 * s))
        )

        # Draw a stylized transmission notepad page in deep twilight blue (#162032)
        doc_x0 = int(52 * s)
        doc_y0 = int(58 * s)
        doc_x1 = int(176 * s)
        doc_y1 = int(204 * s)
        doc_radius = max(2, int(14 * s))

        draw.rounded_rectangle(
            [doc_x0, doc_y0, doc_x1, doc_y1],
            radius=doc_radius,
            fill=(22, 32, 50, 255),
            outline=(88, 166, 255, 200),  # Nebula cyan border
            width=max(1, int(5 * s))
        )

        # Notepad transmission lines in soft cyan / starlight white
        line_x0 = int(72 * s)
        line_x1 = int(156 * s)
        line_ys = [int(94 * s), int(122 * s), int(150 * s), int(176 * s)]
        line_widths = [line_x1 - line_x0, int(70 * s), int(64 * s), int(45 * s)]

        line_color = (121, 192, 255, 230)
        for y, lw in zip(line_ys, line_widths):
            h = max(1, int(6 * s))
            draw.rounded_rectangle(
                [line_x0, y, line_x0 + lw, y + h],
                radius=max(1, int(3 * s)),
                fill=line_color
            )

        # Radiant golden star perched on the top-right corner
        star_cx = int(185 * s)
        star_cy = int(72 * s)
        r_out = int(42 * s)
        r_in = int(18 * s)
        draw_star(draw, star_cx, star_cy, r_out, r_in, points=5, 
                  fill=(242, 204, 96, 255), 
                  outline=(255, 235, 150, 255), 
                  width=max(1, int(2 * s)))

        # Little cosmic sparkle in the lower-right area
        sparkle_x = int(208 * s)
        sparkle_y = int(190 * s)
        sp_r = int(10 * s)
        if sp_r >= 2:
            gold = (242, 204, 96, 255)
            w_sp = max(1, int(2 * s))
            draw.line([(sparkle_x - sp_r, sparkle_y), (sparkle_x + sp_r, sparkle_y)], fill=gold, width=w_sp)
            draw.line([(sparkle_x, sparkle_y - sp_r), (sparkle_x, sparkle_y + sp_r)], fill=gold, width=w_sp)

        images.append(img)

    # Save as multi-resolution icon
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    images[0].save(
        output_path, 
        format="ICO", 
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )
    print(f"✨ StellarNotes icon created successfully: {output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(current_dir, "assets")
    output_ico = os.path.join(assets_dir, "stellar_notes.ico")
    create_stellar_icon(output_ico)
