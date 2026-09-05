# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: generate_icon.py
# ☆ Description: Generates multi-resolution .ico & .png assets: Alien Ship with Network Signals
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
    start_angle = -math.pi / 2
    for i in range(2 * points):
        r = r_outer if i % 2 == 0 else r_inner
        ang = start_angle + i * angle_step
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        poly.append((x, y))
    draw.polygon(poly, fill=fill, outline=outline, width=width)


def draw_arc_segment(draw, cx, cy, radius, start_deg, end_deg, color, width=3):
    """Draws an arc line segment with specified thickness."""
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
    draw.arc(bbox, start=start_deg, end=end_deg, fill=color, width=width)


def create_network_visor_icon(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    ico_path = os.path.join(output_dir, "network_info.ico")
    png_path = os.path.join(output_dir, "network_info.png")

    sizes = [(256, 256), (48, 48), (32, 32), (16, 16)]
    images = []

    for width, height in sizes:
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        s = width / 256.0

        # ----------------------------------------------------------------------
        # 1. Background Badge: Deep Space Obsidian (#0d1117)
        # ----------------------------------------------------------------------
        pad = int(8 * s)
        corner_radius = int(46 * s)
        badge_box = [pad, pad, width - pad, height - pad]
        draw.rounded_rectangle(
            badge_box,
            radius=corner_radius,
            fill=(13, 17, 23, 255),
            outline=(88, 166, 255, 255),  # Starlight Cyan border
            width=max(1, int(7 * s))
        )

        if width >= 32:
            inner_pad = int(14 * s)
            draw.rounded_rectangle(
                [inner_pad, inner_pad, width - inner_pad, height - inner_pad],
                radius=max(2, corner_radius - int(6 * s)),
                fill=None,
                outline=(28, 38, 54, 180),
                width=max(1, int(2 * s))
            )

        # ----------------------------------------------------------------------
        # 2. Concentric Network Signal Waves (Radiating from Alien Antenna)
        # ----------------------------------------------------------------------
        # Center of antenna transmitter
        tx_cx = int(128 * s)
        tx_cy = int(88 * s)

        # Signal Arc 1 (Inner Cyan)
        r1 = int(32 * s)
        draw_arc_segment(draw, tx_cx, tx_cy, r1, 205, 335, (88, 166, 255, 240), width=max(1, int(5 * s)))

        # Signal Arc 2 (Middle Celestial Gold)
        r2 = int(54 * s)
        draw_arc_segment(draw, tx_cx, tx_cy, r2, 215, 325, (242, 204, 96, 240), width=max(1, int(6 * s)))

        # Signal Arc 3 (Outer Nebula Magenta)
        r3 = int(76 * s)
        draw_arc_segment(draw, tx_cx, tx_cy, r3, 225, 315, (188, 140, 255, 220), width=max(1, int(5 * s)))

        # ----------------------------------------------------------------------
        # 3. Sub-Space Transmission Beams (Radiating below the Alien Ship)
        # ----------------------------------------------------------------------
        beam_cx = int(128 * s)
        beam_cy = int(178 * s)

        # Conical Sub-Space Tractor Transmission Beam
        beam_poly = [
            (beam_cx - int(12 * s), beam_cy),
            (beam_cx + int(12 * s), beam_cy),
            (beam_cx + int(56 * s), int(226 * s)),
            (beam_cx - int(56 * s), int(226 * s))
        ]
        draw.polygon(beam_poly, fill=(88, 166, 255, 35))

        # Bottom network telemetry ground pulse lines
        if width >= 32:
            draw.line([(beam_cx - int(42 * s), int(212 * s)), (beam_cx + int(42 * s), int(212 * s))], fill=(88, 166, 255, 140), width=max(1, int(3 * s)))
            draw.line([(beam_cx - int(24 * s), int(224 * s)), (beam_cx + int(24 * s), int(224 * s))], fill=(126, 231, 135, 180), width=max(1, int(3 * s)))

        # ----------------------------------------------------------------------
        # 4. Alien Ship (Flying Saucer / UFO)
        # ----------------------------------------------------------------------
        ship_cx = int(128 * s)
        ship_cy = int(152 * s)

        # Saucer Lower Hull Flange (Shadow / Keel)
        hull_bot_bbox = [
            ship_cx - int(78 * s),
            ship_cy - int(4 * s),
            ship_cx + int(78 * s),
            ship_cy + int(26 * s)
        ]
        draw.ellipse(hull_bot_bbox, fill=(22, 28, 40, 255), outline=(48, 64, 90, 255), width=max(1, int(2 * s)))

        # Saucer Main Metallic Disc (Twilight Slate with Starlight Cyan Edge)
        disc_bbox = [
            ship_cx - int(82 * s),
            ship_cy - int(18 * s),
            ship_cx + int(82 * s),
            ship_cy + int(16 * s)
        ]
        draw.ellipse(disc_bbox, fill=(30, 41, 59, 255), outline=(88, 166, 255, 255), width=max(1, int(5 * s)))

        # Saucer Top Cockpit Bubble Canopy (Glowing Glass Dome)
        dome_w = int(38 * s)
        dome_h = int(32 * s)
        dome_bbox = [
            ship_cx - dome_w,
            ship_cy - int(14 * s) - dome_h,
            ship_cx + dome_w,
            ship_cy - int(4 * s)
        ]
        draw.chord(dome_bbox, start=180, end=360, fill=(20, 36, 56, 255), outline=(121, 192, 255, 255), width=max(1, int(3 * s)))

        # Alien Pilot Inside Cockpit Canopy
        alien_cx = ship_cx
        alien_cy = ship_cy - int(24 * s)
        alien_rx = int(14 * s)
        alien_ry = int(12 * s)

        # Little Alien Head (Alien Mint Green #7ee787)
        draw.ellipse(
            [alien_cx - alien_rx, alien_cy - alien_ry, alien_cx + alien_rx, alien_cy + alien_ry],
            fill=(126, 231, 135, 255)
        )

        # Cute Alien Black Oval Eyes
        eye_rx = max(1, int(4 * s))
        eye_ry = max(1, int(5 * s))
        draw.ellipse([alien_cx - int(7 * s) - eye_rx, alien_cy - eye_ry, alien_cx - int(7 * s) + eye_rx, alien_cy + eye_ry], fill=(13, 17, 23, 255))
        draw.ellipse([alien_cx + int(7 * s) - eye_rx, alien_cy - eye_ry, alien_cx + int(7 * s) + eye_rx, alien_cy + eye_ry], fill=(13, 17, 23, 255))

        # Little white reflection dots in eyes
        if width >= 48:
            dot_r = max(1, int(1.5 * s))
            draw.ellipse([alien_cx - int(7 * s) - dot_r, alien_cy - int(2 * s) - dot_r, alien_cx - int(7 * s) + dot_r, alien_cy - int(2 * s) + dot_r], fill=(255, 255, 255, 255))
            draw.ellipse([alien_cx + int(7 * s) - dot_r, alien_cy - int(2 * s) - dot_r, alien_cx + int(7 * s) + dot_r, alien_cy - int(2 * s) + dot_r], fill=(255, 255, 255, 255))

        # Glass dome highlight reflection streak
        if width >= 32:
            glare_bbox = [ship_cx - int(28 * s), ship_cy - int(42 * s), ship_cx + int(10 * s), ship_cy - int(24 * s)]
            draw.arc(glare_bbox, start=210, end=290, fill=(255, 255, 255, 200), width=max(1, int(2 * s)))

        # Antenna Rod extending above dome
        antenna_top_y = tx_cy
        draw.line([(ship_cx, ship_cy - int(44 * s)), (ship_cx, antenna_top_y)], fill=(226, 232, 240, 255), width=max(1, int(4 * s)))

        # Glowing Transmitter Beacon Orb atop antenna
        orb_r = max(2, int(6 * s))
        draw.ellipse(
            [ship_cx - orb_r, antenna_top_y - orb_r, ship_cx + orb_r, antenna_top_y + orb_r],
            fill=(242, 204, 96, 255),
            outline=(255, 255, 255, 255),
            width=max(1, int(2 * s))
        )

        # Saucer Porthole LEDs / Thruster Lights along the rim
        led_offsets = [-60, -36, -12, 12, 36, 60]
        led_colors = [
            (242, 204, 96, 255),   # Gold
            (88, 166, 255, 255),   # Cyan
            (126, 231, 135, 255),  # Mint
            (126, 231, 135, 255),  # Mint
            (88, 166, 255, 255),   # Cyan
            (242, 204, 96, 255)    # Gold
        ]
        for dx, col in zip(led_offsets, led_colors):
            x = ship_cx + int(dx * s)
            # Elliptical path along saucer contour
            dy = int(10 * s * (1.0 - (abs(dx) / 75.0)**2)**0.5)
            y = ship_cy + dy
            lr = max(1, int(4 * s))
            draw.ellipse([x - lr, y - lr, x + lr, y + lr], fill=col, outline=(255, 255, 255, 220), width=max(1, int(1 * s)))

        # ----------------------------------------------------------------------
        # 5. Cosmic Stars & Sparkles
        # ----------------------------------------------------------------------
        # Celestial Star in Top Right
        draw_star(draw, int(208 * s), int(48 * s), int(22 * s), int(9 * s), points=5,
                  fill=(242, 204, 96, 255), outline=(255, 245, 180, 255), width=max(1, int(1 * s)))

        # Small Starlight Cross in Top Left
        if width >= 48:
            draw_star(draw, int(48 * s), int(58 * s), int(14 * s), int(5 * s), points=4,
                      fill=(88, 166, 255, 230))

            # Sparkle dots
            dot_r = max(1, int(2 * s))
            draw.ellipse([int(40 * s) - dot_r, int(120 * s) - dot_r, int(40 * s) + dot_r, int(120 * s) + dot_r], fill=(126, 231, 135, 220))
            draw.ellipse([int(218 * s) - dot_r, int(130 * s) - dot_r, int(218 * s) + dot_r, int(130 * s) + dot_r], fill=(242, 204, 96, 220))

        images.append(img)

    # Save 256x256 image as primary PNG
    images[0].save(png_path, format="PNG")

    # Save multi-resolution ICO file
    images[0].save(
        ico_path,
        format="ICO",
        sizes=[(256, 256), (48, 48), (32, 32), (16, 16)],
        append_images=images[1:]
    )

    print(f"✨ Successfully generated Alien Ship & Network Signal icons:")
    print(f"   [+] ICO: {ico_path}")
    print(f"   [+] PNG: {png_path}")
    return ico_path, png_path


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    create_network_visor_icon(assets_dir)
