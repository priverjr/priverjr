"""Generate the profile banner locally. Requires Pillow; no external services."""
from pathlib import Path
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1200, 360


def font(size, bold=False):
    family = "Liberation Sans:style=Bold" if bold else "Liberation Sans"
    path = subprocess.check_output(["fc-match", "-f", "%{file}", family], text=True)
    return ImageFont.truetype(path, size)


def frame(index):
    im = Image.new("RGB", (WIDTH, HEIGHT), "#0b1220")
    d = ImageDraw.Draw(im)
    for x in range(0, WIDTH, 40):
        d.line((x, 0, x, HEIGHT), fill="#111e30")
    for y in range(0, HEIGHT, 40):
        d.line((0, y, WIDTH, y), fill="#111e30")
    d.rounded_rectangle((1, 1, WIDTH-2, HEIGHT-2), radius=20, outline="#29425a", width=2)
    d.rectangle((56, 58, 61, 302), fill="#67e8f9")
    d.text((86, 59), "PRIVERJR  /  ENGINEERING & INNOVATION", font=font(19, True), fill="#67e8f9")
    d.text((82, 106), "Privatus Cosmas", font=font(66, True), fill="#f1f5f9")
    d.text((86, 190), "Software Engineer  /  Full-Stack & Mobile", font=font(27), fill="#ced9e7")
    d.text((86, 242), "WEB   ·   MOBILE   ·   AI   ·   BUSINESS SYSTEMS", font=font(19, True), fill="#90a6be")
    d.text((86, 291), "MBEYA, TANZANIA   /   depriver.tech", font=font(17), fill="#90a6be")
    # A restrained orbit animation keeps the identity readable in every frame.
    cx, cy = 1040, 178
    for radius in (58, 89, 119):
        d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline="#29425a", width=2)
    d.text((1005, 154), "</>", font=font(38, True), fill="#67e8f9")
    for j, radius in enumerate((58, 89, 119)):
        angle = 2 * math.pi * (index / 60 + j / 3)
        x, y = cx + radius * math.cos(angle), cy + radius * math.sin(angle)
        d.ellipse((x-6, y-6, x+6, y+6), fill=("#67e8f9", "#a78bfa", "#67e8f9")[j])
    return im


if __name__ == "__main__":
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    frames = [frame(i) for i in range(60)]
    frames[0].save(assets / "profile-banner.png")
    frames[0].save(assets / "profile-banner.gif", save_all=True,
                   append_images=frames[1:], duration=100, loop=0, optimize=True)
    print(f"Created {assets / 'profile-banner.gif'}")
