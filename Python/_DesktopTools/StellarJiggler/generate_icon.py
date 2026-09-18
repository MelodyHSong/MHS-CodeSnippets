# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: generate_icon.py
# ☆ Description: Generates multi-resolution .ico asset for StellarJiggler
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


def create_jiggler_icon(output_path):
    """Synthesizes a multi-resolution Windows .ico file with cosmic mouse jiggler styling."""
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
            width=max(1, int(7 * s))
        )

        # Inner workstation console frame (#161b22)
        inner_pad = max(2, int(26 * s))
        inner_box = [inner_pad, inner_pad, width - inner_pad, height - inner_pad]
        draw.rounded_rectangle(
            inner_box,
            radius=max(2, int(24 * s)),
            fill=(22, 27, 34, 255),
            outline=(48, 54, 61, 255),   # Rim border
            width=max(1, int(3 * s))
        )

        # Orbital motion rings (representing continuous celestial jiggling)
        cx = width / 2.0
        cy = height / 2.0
        orbit_rx = 76 * s
        orbit_ry = 34 * s

        # Tilted celestial orbit path
        for ang_deg in range(0, 360, 18):
            ang = math.radians(ang_deg)
            # Tilt orbit slightly
            ox = cx + orbit_rx * math.cos(ang) * 0.9 - orbit_ry * math.sin(ang) * 0.4
            oy = cy + orbit_rx * math.cos(ang) * 0.3 + orbit_ry * math.sin(ang) * 0.9
            dot_size = max(1.0, 3.5 * s)
            draw.ellipse([ox - dot_size, oy - dot_size, ox + dot_size, oy + dot_size], fill=(88, 166, 255, 120))

        # Mouse Body Silhouette (ergonomic rounded computer mouse shape)
        mouse_w = 78 * s
        mouse_h = 114 * s
        mx0 = cx - mouse_w / 2.0
        my0 = cy - mouse_h / 2.0 + 4 * s
        mx1 = cx + mouse_w / 2.0
        my1 = cy + mouse_h / 2.0 + 4 * s
        mouse_radius = int(36 * s)

        draw.rounded_rectangle(
            [mx0, my0, mx1, my1],
            radius=mouse_radius,
            fill=(33, 38, 45, 255),
            outline=(88, 166, 255, 230),
            width=max(1, int(4 * s))
        )

        # Mouse button divider line
        div_y = my0 + 44 * s
        draw.line([mx0 + 4 * s, div_y, mx1 - 4 * s, div_y], fill=(48, 54, 61, 255), width=max(1, int(3 * s)))
        draw.line([cx, my0 + 6 * s, cx, div_y], fill=(48, 54, 61, 255), width=max(1, int(3 * s)))

        # Mouse Scroll Wheel / Glowing Core (Celestial Amber)
        wheel_w = max(2, int(8 * s))
        wheel_h = max(4, int(20 * s))
        wy0 = my0 + 12 * s
        draw.rounded_rectangle(
            [cx - wheel_w, wy0, cx + wheel_w, wy0 + wheel_h],
            radius=max(1, int(4 * s)),
            fill=(242, 204, 96, 255),
            outline=(255, 240, 180, 255),
            width=max(1, int(2 * s))
        )

        # Glowing Celestial Star in lower body of mouse
        star_cy = cy + 28 * s
        draw_star(
            draw, cx, star_cy, 22 * s, 10 * s, points=5,
            fill=(242, 204, 96, 255),
            outline=(255, 245, 180, 255),
            width=max(1, int(2 * s))
        )

        # Pulse Sparkle Dots around cursor
        if width >= 48:
            # Mint activity indicator in top right
            pulse_x = cx + 58 * s
            pulse_y = cy - 58 * s
            p_rad = max(2, int(7 * s))
            draw.ellipse([pulse_x - p_rad, pulse_y - p_rad, pulse_x + p_rad, pulse_y + p_rad], fill=(126, 231, 135, 255))
            draw.ellipse([pulse_x - p_rad - 3 * s, pulse_y - p_rad - 3 * s, pulse_x + p_rad + 3 * s, pulse_y + p_rad + 3 * s],
                         outline=(126, 231, 135, 90), width=max(1, int(2 * s)))

            # Small 4-pointed stars on the orbit trail
            draw_star(draw, cx - 62 * s, cy - 20 * s, 11 * s, 4 * s, points=4, fill=(88, 166, 255, 220))
            draw_star(draw, cx + 64 * s, cy + 30 * s, 9 * s, 3 * s, points=4, fill=(188, 140, 255, 220))

        images.append(img)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
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
    create_jiggler_icon(output_ico)


if __name__ == "__main__":
    main()
