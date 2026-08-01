"""Gera a capa animada usada no README do projeto.

Uso local:
    pip install pillow
    python tools/gerar_capa_readme.py

Saída:
    assets/capa_dissertacao_entropia.gif
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 800, 320
FRAME_COUNT = 21
FRAME_DURATION_MS = 190

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "capa_dissertacao_entropia.gif"

NAVY = (8, 20, 42)
NAVY_2 = (13, 36, 68)
CYAN = (45, 212, 191)
BLUE = (80, 170, 255)
AMBER = (255, 184, 77)
WHITE = (245, 249, 255)
MUTED = (174, 193, 216)
GRID = (55, 82, 112)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Carrega uma fonte comum em Linux; usa a fonte padrão como fallback."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


FONT_BADGE = load_font(11, True)
FONT_TITLE = load_font(20, True)
FONT_SUBTITLE = load_font(12)
FONT_SMALL = load_font(9)
FONT_SMALL_BOLD = load_font(9, True)
FONT_FORMULA = load_font(14)
FONT_AUTHOR = load_font(11, True)


def smoothstep(value: float) -> float:
    return 3 * value**2 - 2 * value**3


def simulation_progress(frame: int) -> float:
    """Avança da condição concentrada ao equilíbrio e pausa antes do reinício."""
    normalized = frame / (FRAME_COUNT - 1)
    if normalized < 0.74:
        return smoothstep(normalized / 0.74)
    return 1.0


def restart_fade(frame: int) -> float:
    normalized = frame / (FRAME_COUNT - 1)
    return max(0.0, (normalized - 0.90) / 0.10)


def make_background() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    pixels = image.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            rx = x / WIDTH
            ry = y / HEIGHT
            glow = max(0.0, 1 - math.hypot((x - 225) / 470, (y - 120) / 310))
            pixels[x, y] = (
                min(255, int(NAVY[0] * (1 - rx) + NAVY_2[0] * rx + 8 * glow)),
                min(255, int(NAVY[1] * (1 - ry) + NAVY_2[1] * ry + 16 * glow)),
                min(255, int(NAVY[2] + 15 * rx + 20 * glow)),
            )
    return image


BACKGROUND = make_background()

random.seed(2026)
PARTICLES: list[tuple[float, float, float, float, float]] = []
for _ in range(38):
    initial_x = random.uniform(47, 147)
    initial_y = random.uniform(84, 168)
    final_x = (
        random.uniform(47, 147)
        if random.random() < 0.5
        else random.uniform(200, 300)
    )
    final_y = random.uniform(84, 168)
    PARTICLES.append(
        (initial_x, initial_y, final_x, final_y, random.uniform(0, math.tau))
    )


def create_frame(frame: int) -> Image.Image:
    image = BACKGROUND.copy().convert("RGBA")
    draw = ImageDraw.Draw(image, "RGBA")
    progress = simulation_progress(frame)

    for x in range(0, WIDTH, 32):
        draw.line((x, 0, x, HEIGHT), fill=(*GRID, 22))
    for y in range(0, HEIGHT, 32):
        draw.line((0, y, WIDTH, y), fill=(*GRID, 18))

    draw.rounded_rectangle(
        (25, 39, 333, 283), radius=19, fill=(5, 17, 34, 188),
        outline=(*BLUE, 90), width=2,
    )
    draw.text((44, 53), "MODELO DE EHRENFEST", font=FONT_SMALL_BOLD, fill=CYAN)
    draw.text((44, 67), "partículas → equilíbrio estatístico", font=FONT_SMALL, fill=MUTED)

    left_chamber = (44, 80, 159, 181)
    right_chamber = (188, 80, 303, 181)
    for chamber in (left_chamber, right_chamber):
        draw.rounded_rectangle(
            chamber, radius=15, fill=(17, 46, 78, 225),
            outline=(*BLUE, 180), width=1,
        )
    draw.rectangle((159, 116, 188, 145), fill=(17, 46, 78, 225), outline=(*BLUE, 120))
    draw.text((82, 89), "A", font=FONT_SMALL_BOLD, fill=WHITE)
    draw.text((226, 89), "B", font=FONT_SMALL_BOLD, fill=WHITE)

    for index, (x0, y0, x1, y1, phase) in enumerate(PARTICLES):
        local = min(1.0, max(0.0, (progress - index / 38 * 0.16) / 0.84))
        local = smoothstep(local)
        x = x0 + (x1 - x0) * local
        y = y0 + (y1 - y0) * local + math.sin(frame * 0.55 + phase) * 1.6
        radius = 3.1 if index % 3 == 0 else 2.6
        color = AMBER if index % 4 == 0 else CYAN
        draw.ellipse(
            (x - radius, y - radius, x + radius, y + radius),
            fill=(*color, 240), outline=(255, 255, 255, 120),
        )

    draw.rounded_rectangle(
        (44, 197, 303, 256), radius=10, fill=(10, 29, 52, 225),
        outline=(255, 255, 255, 38),
    )
    draw.text((54, 203), "ENTROPIA NORMALIZADA", font=FONT_SMALL_BOLD, fill=MUTED)
    origin_x, origin_y = 55, 246
    draw.line((origin_x, origin_y, 293, origin_y), fill=(*MUTED, 100))
    draw.line((origin_x, 218, origin_x, origin_y), fill=(*MUTED, 100))

    point_count = 42
    visible_points = max(2, int(point_count * progress))
    curve: list[tuple[float, float]] = []
    for index in range(visible_points):
        t = index / (point_count - 1)
        entropy = 1 - math.exp(-5.2 * t)
        fluctuation = 0.018 * math.sin(18 * t + 0.7 * frame)
        curve.append((origin_x + t * (293 - origin_x), origin_y - (entropy + fluctuation) * 24))
    draw.line(curve, fill=(*AMBER, 245), width=2)
    end_x, end_y = curve[-1]
    draw.ellipse((end_x - 3, end_y - 3, end_x + 3, end_y + 3), fill=WHITE)
    draw.text(
        (54, 263), "S(t) cresce até o macroestado mais provável",
        font=FONT_SMALL, fill=BLUE,
    )

    draw.rounded_rectangle(
        (355, 39, 775, 283), radius=19, fill=(7, 21, 43, 175),
        outline=(255, 255, 255, 48),
    )
    draw.rounded_rectangle(
        (379, 54, 544, 76), radius=11, fill=(*CYAN, 45), outline=(*CYAN, 150),
    )
    draw.text((389, 59), "PRODUTO EDUCACIONAL", font=FONT_BADGE, fill=WHITE)

    y = 91
    for line in (
        "METODOLOGIA PARA O ENSINO",
        "DE ENTROPIA FÍSICA",
        "VIA NOÇÕES DE TEORIA",
        "DA INFORMAÇÃO",
    ):
        draw.text((379, y), line, font=FONT_TITLE, fill=WHITE)
        y += 25

    draw.rounded_rectangle((379, 192, 732, 195), radius=2, fill=(*BLUE, 185))
    draw.text((379, 207), "S = kᴮ ln Ω", font=FONT_FORMULA, fill=AMBER)
    draw.text((514, 207), "H = −Σ pᵢ log₂ pᵢ", font=FONT_FORMULA, fill=CYAN)
    draw.text((379, 235), "Simulações computacionais em Python", font=FONT_SUBTITLE, fill=MUTED)
    draw.text((379, 258), "MARCOS CAVALCANTE FURTADO", font=FONT_AUTHOR, fill=WHITE)
    draw.text((623, 259), "MNPEF • UNIFAP • 2026", font=FONT_SMALL_BOLD, fill=BLUE)

    fade = restart_fade(frame)
    if fade:
        image = Image.alpha_composite(
            image, Image.new("RGBA", (WIDTH, HEIGHT), (*NAVY, int(255 * fade)))
        )
    return image.convert("RGB")


def save_gif() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames = [create_frame(index) for index in range(FRAME_COUNT)]
    palette_source = frames[len(frames) // 2].quantize(
        colors=48, method=Image.Quantize.MEDIANCUT
    )
    palette = palette_source.getpalette()
    quantized_frames: list[Image.Image] = []
    for frame in frames:
        palette_image = Image.new("P", frame.size)
        palette_image.putpalette(palette)
        quantized_frames.append(
            frame.quantize(palette=palette_image, dither=Image.Dither.NONE)
        )
    quantized_frames[0].save(
        OUTPUT, save_all=True, append_images=quantized_frames[1:],
        duration=FRAME_DURATION_MS, loop=0, optimize=True, disposal=1,
    )
    print(f"Capa criada em: {OUTPUT}")


if __name__ == "__main__":
    save_gif()
