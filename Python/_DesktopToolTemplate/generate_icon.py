# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: generate_icon.py
# ☆ Description: Generates multi-resolution .ico asset for Desktop Tool Template
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


def create_tool_icon(output_path):
    """Synthesizes a multi-resolution Windows .ico file with cosmic tool badge styling."""
    sizes = [(256, 256), (48, 48), (32, 32), (16, 16)]
    images = []

    for width, height in sizes:
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        s = width / 256.0

        # Background rounded badge: Deep space obsidian (#0d1117)
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

        # Inner workstation console frame (#161b22)
        inner_pad = max(2, int(28 * s))
        inner_box = [inner_pad, inner_pad, width - inner_pad, height - inner_pad]
        draw.rounded_rectangle(
            inner_box,
            radius=max(2, int(26 * s)),
            fill=(22, 27, 34, 255),
            outline=(48, 54, 61, 255),   # Rim border
            width=max(1, int(4 * s))
        )

        # Header bar with decorative console dots
        header_y1 = int(68 * s)
        draw.rectangle(
            [inner_pad + int(4 * s), inner_pad + int(4 * s), width - inner_pad - int(4 * s), header_y1],
            fill=(33, 38, 45, 255)
        )

        # 3 console dots (Coral, Gold, Mint)
        dot_r = max(1, int(5 * s))
        dot_colors = [(248, 81, 73, 255), (242, 204, 96, 255), (126, 231, 135, 255)]
        start_x = inner_pad + int(16 * s)
        dot_y = inner_pad + int(18 * s)
        for i, col in enumerate(dot_colors):
            dx = start_x + int(i * 16 * s)
            draw.ellipse([dx - dot_r, dot_y - dot_r, dx + dot_r, dot_y + dot_r], fill=col)

        # Center motif: Radiant Celestial Star with glowing core
        cx = width / 2.0
        cy = (height / 2.0) + (14 * s)
        r_out = 52 * s
        r_in = 24 * s

        # Outer glow ring
        glow_r = int(64 * s)
        draw.ellipse(
            [cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r],
            outline=(88, 166, 255, 60),
            width=max(1, int(4 * s))
        )

        # Main radiant star in golden celestial amber
        draw_star(
            draw, cx, cy, r_out, r_in, points=5,
            fill=(242, 204, 96, 255),
            outline=(255, 235, 150, 255),
            width=max(1, int(3 * s))
        )

        # Small diamond sparkle in upper right
        if width >= 48:
            sp_x = cx + int(60 * s)
            sp_y = cy - int(44 * s)
            draw_star(draw, sp_x, sp_y, int(16 * s), int(6 * s), points=4,
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
    print(f"[✓] Successfully generated multi-resolution icon at:\n    {output_path}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    output_ico = os.path.join(assets_dir, "app_icon.ico")
    create_tool_icon(output_ico)


if __name__ == "__main__":
    main()
