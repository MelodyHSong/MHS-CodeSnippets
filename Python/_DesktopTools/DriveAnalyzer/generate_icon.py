# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: generate_icon.py
# ☆ Description: Generates multi-resolution .ico asset for Stellar Snooper
# ☆ Featuring a cute cosmic alien snooper with a magnifying glass!
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

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("[!] Pillow is not installed. Please install it with: pip install pillow")
    sys.exit(1)


def draw_star(draw, cx, cy, r_outer, r_inner, points=5, fill=(242, 204, 96, 255), outline=None, width=1):
    """Draws a star polygon given center, outer radius, and inner radius."""
    poly = []
    angle_step = math.pi / points
    start_angle = -math.pi / 2
    for i in range(2 * points):
        r = r_outer if i % 2 == 0 else r_inner
        ang = start_angle + i * angle_step
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        poly.append((x, y))
    draw.polygon(poly, fill=fill, outline=outline, width=width)


def create_stellar_snooper_icon(output_path):
    """Synthesizes a multi-resolution Windows .ico file with a cute alien snooper holding a magnifying glass."""
    sizes = [(256, 256), (48, 48), (32, 32), (16, 16)]
    images = []

    for width, height in sizes:
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        s = width / 256.0

        # 1. Background rounded badge: Deep space obsidian (#0d1117)
        pad = max(1, int(8 * s))
        corner_radius = max(3, int(46 * s))
        badge_box = [pad, pad, width - pad, height - pad]
        draw.rounded_rectangle(
            badge_box,
            radius=corner_radius,
            fill=(13, 17, 23, 255),
            outline=(88, 166, 255, 255),  # Starlight Cyan border
            width=max(1, int(8 * s))
        )

        # 2. Inner workstation console frame (#161b22)
        inner_pad = max(2, int(26 * s))
        inner_box = [inner_pad, inner_pad, width - inner_pad, height - inner_pad]
        draw.rounded_rectangle(
            inner_box,
            radius=max(2, int(24 * s)),
            fill=(22, 27, 34, 255),
            outline=(48, 54, 61, 255),   # Rim border
            width=max(1, int(4 * s))
        )

        # 3. Header bar with decorative console dots
        header_y1 = int(60 * s)
        draw.rectangle(
            [inner_pad + int(4 * s), inner_pad + int(4 * s), width - inner_pad - int(4 * s), header_y1],
            fill=(33, 38, 45, 255)
        )

        # 3 console dots (Coral, Gold, Mint)
        dot_r = max(1, int(4.5 * s))
        dot_colors = [(248, 81, 73, 255), (242, 204, 96, 255), (126, 231, 135, 255)]
        start_x = inner_pad + int(14 * s)
        dot_y = inner_pad + int(16 * s)
        for i, col in enumerate(dot_colors):
            dx = start_x + int(i * 15 * s)
            draw.ellipse([dx - dot_r, dot_y - dot_r, dx + dot_r, dot_y + dot_r], fill=col)

        # 4. Cute Alien Snooper
        # Center coordinates of the character
        cx = width / 2.0 - int(10 * s)
        cy = (height / 2.0) + int(24 * s)

        # Antennae stalks & Star Baubles
        ant_left_start = (cx - int(24 * s), cy - int(38 * s))
        ant_left_end = (cx - int(40 * s), cy - int(66 * s))
        ant_right_start = (cx + int(24 * s), cy - int(38 * s))
        ant_right_end = (cx + int(40 * s), cy - int(66 * s))

        draw.line([ant_left_start, ant_left_end], fill=(126, 231, 135, 255), width=max(1, int(4 * s)))
        draw.line([ant_right_start, ant_right_end], fill=(126, 231, 135, 255), width=max(1, int(4 * s)))

        # Antenna tips: glowing gold stars or baubles
        bauble_r = max(2, int(8 * s))
        draw.ellipse([ant_left_end[0] - bauble_r, ant_left_end[1] - bauble_r,
                      ant_left_end[0] + bauble_r, ant_left_end[1] + bauble_r],
                     fill=(242, 204, 96, 255), outline=(255, 235, 150, 255), width=max(1, int(1.5 * s)))
        draw.ellipse([ant_right_end[0] - bauble_r, ant_right_end[1] - bauble_r,
                      ant_right_end[0] + bauble_r, ant_right_end[1] + bauble_r],
                     fill=(242, 204, 96, 255), outline=(255, 235, 150, 255), width=max(1, int(1.5 * s)))

        # Alien Head (cute rounded shape)
        head_rx = int(50 * s)
        head_ry = int(42 * s)
        head_box = [cx - head_rx, cy - head_ry, cx + head_rx, cy + head_ry]
        draw.ellipse(head_box, fill=(126, 231, 135, 255), outline=(88, 196, 110, 255), width=max(1, int(3 * s)))

        # Cheek Blushes (cute soft coral pink)
        blush_rx = max(2, int(9 * s))
        blush_ry = max(1, int(5 * s))
        draw.ellipse([cx - int(34 * s) - blush_rx, cy + int(10 * s) - blush_ry,
                      cx - int(34 * s) + blush_rx, cy + int(10 * s) + blush_ry],
                     fill=(248, 120, 110, 200))
        draw.ellipse([cx + int(16 * s) - blush_rx, cy + int(10 * s) - blush_ry,
                      cx + int(16 * s) + blush_rx, cy + int(10 * s) + blush_ry],
                     fill=(248, 120, 110, 200))

        # Big Cute Alien Eyes
        eye_w = max(2, int(12 * s))
        eye_h = max(3, int(17 * s))

        # Left eye
        left_eye_cx = cx - int(20 * s)
        left_eye_cy = cy - int(4 * s)
        draw.ellipse([left_eye_cx - eye_w, left_eye_cy - eye_h,
                      left_eye_cx + eye_w, left_eye_cy + eye_h],
                     fill=(13, 17, 23, 255))
        # Left eye glossy highlights
        draw.ellipse([left_eye_cx - max(1, int(5 * s)), left_eye_cy - max(2, int(8 * s)),
                      left_eye_cx + max(1, int(2 * s)), left_eye_cy - max(1, int(1 * s))],
                     fill=(255, 255, 255, 255))
        if width >= 32:
            draw.ellipse([left_eye_cx + max(1, int(1 * s)), left_eye_cy + max(1, int(4 * s)),
                          left_eye_cx + max(1, int(4 * s)), left_eye_cy + max(2, int(7 * s))],
                         fill=(255, 255, 255, 200))

        # Right eye (winking or looking curiously through the magnifying glass)
        right_eye_cx = cx + int(14 * s)
        right_eye_cy = cy - int(4 * s)
        draw.ellipse([right_eye_cx - eye_w, right_eye_cy - eye_h,
                      right_eye_cx + eye_w, right_eye_cy + eye_h],
                     fill=(13, 17, 23, 255))
        # Right eye glossy highlights
        draw.ellipse([right_eye_cx - max(1, int(5 * s)), right_eye_cy - max(2, int(8 * s)),
                      right_eye_cx + max(1, int(2 * s)), right_eye_cy - max(1, int(1 * s))],
                     fill=(255, 255, 255, 255))
        if width >= 32:
            draw.ellipse([right_eye_cx + max(1, int(1 * s)), right_eye_cy + max(1, int(4 * s)),
                          right_eye_cx + max(1, int(4 * s)), right_eye_cy + max(2, int(7 * s))],
                         fill=(255, 255, 255, 200))

        # Cute little smiling mouth
        mouth_w = max(2, int(8 * s))
        mouth_y = cy + int(14 * s)
        draw.arc([cx - int(8 * s) - mouth_w, mouth_y - max(1, int(4 * s)),
                  cx - int(8 * s) + mouth_w, mouth_y + max(2, int(6 * s))],
                 start=0, end=180, fill=(13, 17, 23, 255), width=max(1, int(2.5 * s)))

        # 5. Magnifying Glass (Snooper's tool!)
        mag_cx = cx + int(48 * s)
        mag_cy = cy + int(8 * s)
        mag_r = int(32 * s)

        # Magnifying glass handle
        handle_start = (mag_cx + int(22 * s), mag_cy + int(22 * s))
        handle_end = (mag_cx + int(48 * s), mag_cy + int(48 * s))
        draw.line([handle_start, handle_end], fill=(242, 204, 96, 255), width=max(2, int(7 * s)))
        draw.line([handle_start, handle_end], fill=(180, 140, 50, 255), width=max(1, int(3 * s)))

        # Cute alien paw holding the handle
        paw_cx = handle_start[0] + int(8 * s)
        paw_cy = handle_start[1] + int(8 * s)
        paw_r = max(2, int(7 * s))
        draw.ellipse([paw_cx - paw_r, paw_cy - paw_r, paw_cx + paw_r, paw_cy + paw_r],
                     fill=(126, 231, 135, 255), outline=(88, 196, 110, 255), width=max(1, int(1.5 * s)))

        # Lens glass surface (translucent glowing cyan)
        draw.ellipse([mag_cx - mag_r, mag_cy - mag_r, mag_cx + mag_r, mag_cy + mag_r],
                     fill=(88, 166, 255, 80))

        # Magnified discovery inside the lens: a sparkling star!
        if width >= 32:
            draw_star(draw, mag_cx, mag_cy, int(14 * s), int(6 * s), points=4,
                      fill=(255, 255, 255, 250), outline=(242, 204, 96, 255), width=1)

        # Glass highlight glare arc
        draw.arc([mag_cx - int(24 * s), mag_cy - int(24 * s),
                  mag_cx + int(24 * s), mag_cy + int(24 * s)],
                 start=210, end=310, fill=(255, 255, 255, 220), width=max(1, int(3 * s)))

        # Lens Golden Metallic Rim
        draw.ellipse([mag_cx - mag_r, mag_cy - mag_r, mag_cx + mag_r, mag_cy + mag_r],
                     outline=(242, 204, 96, 255), width=max(1, int(4 * s)))
        draw.ellipse([mag_cx - mag_r, mag_cy - mag_r, mag_cx + mag_r, mag_cy + mag_r],
                     outline=(255, 235, 150, 255), width=max(1, int(1.5 * s)))

        # Sparkle in top right corner
        if width >= 48:
            sp_x = width - inner_pad - int(20 * s)
            sp_y = inner_pad + int(24 * s)
            draw_star(draw, sp_x, sp_y, int(12 * s), int(4 * s), points=4,
                      fill=(88, 166, 255, 240), outline=(255, 255, 255, 255), width=1)

        images.append(img)

    # Ensure target directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Save as multi-resolution ICO file
    images[0].save(
        output_path,
        format="ICO",
        sizes=[(im.width, im.height) for im in images],
        append_images=images[1:]
    )
    print(f"[✓] Successfully generated Stellar Snooper icon at:\n    {output_path}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    output_ico = os.path.join(assets_dir, "app_icon.ico")
    create_stellar_snooper_icon(output_ico)


if __name__ == "__main__":
    main()
