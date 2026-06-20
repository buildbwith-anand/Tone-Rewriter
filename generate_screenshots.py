"""Generate macOS-style terminal screenshots for LinkedIn."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).parent / "screenshots"
OUT_DIR.mkdir(exist_ok=True)

# One Dark color palette
BG       = (40,  44,  52)
TITLEBAR = (33,  37,  43)
GRAY     = (92,  99, 112)
TEXT     = (171,178,191)
WHITE    = (235,235,235)
GREEN    = (152,195,121)
YELLOW   = (229,192,123)
BLUE     = (97, 175,239)
CYAN     = (86, 182,194)
RED      = (224,108,117)
ORANGE   = (209,154,102)

FONT_PATH  = "/System/Library/Fonts/SFNSMono.ttf"
FONT_SIZE  = 15
LINE_H     = 24
PAD_X      = 44
PAD_Y      = 22
TITLE_H    = 42
WIDTH      = 900
CORNER_R   = 10


def font(size=FONT_SIZE):
    return ImageFont.truetype(FONT_PATH, size)


def wrap(text, max_chars=88):
    """Split a long string into lines of max_chars."""
    if len(text) <= max_chars:
        return [text]
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).lstrip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build_lines(raw):
    """Expand entries with long text into multiple lines with same color."""
    out = []
    for text, color in raw:
        for line in wrap(text):
            out.append((line, color))
    return out


def draw_terminal(lines_raw, title, filename):
    lines = build_lines(lines_raw)
    height = TITLE_H + PAD_Y + len(lines) * LINE_H + PAD_Y + 12

    img  = Image.new("RGB", (WIDTH, height), BG)
    draw = ImageDraw.Draw(img, "RGBA")
    f    = font()
    f_sm = font(12)

    # -- title bar --
    draw.rounded_rectangle([0, 0, WIDTH, TITLE_H], radius=CORNER_R, fill=TITLEBAR)
    draw.rectangle([0, CORNER_R, WIDTH, TITLE_H], fill=TITLEBAR)   # flatten bottom edge

    # traffic lights
    cy = TITLE_H // 2
    draw.ellipse([16, cy-7, 30, cy+7], fill=(237,106, 94))  # red
    draw.ellipse([38, cy-7, 52, cy+7], fill=(245,191, 79))  # yellow
    draw.ellipse([60, cy-7, 74, cy+7], fill=(98, 197, 84))  # green

    # title
    draw.text((WIDTH // 2, cy), title, fill=GRAY, font=f_sm, anchor="mm")

    # -- terminal body lines --
    y = TITLE_H + PAD_Y
    for text, color in lines:
        if text.strip():
            draw.text((PAD_X, y), text, fill=color, font=f)
        y += LINE_H

    # rounded bottom corners (mask)
    mask = Image.new("L", (WIDTH, height), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, WIDTH, height], radius=CORNER_R, fill=255)
    img.putalpha(mask)

    out = OUT_DIR / filename
    img.save(out, "PNG")
    print(f"  Saved {out}")
    return out


# -----------------------------------------------------------------------
# Screenshot 1 - Professional tone
# -----------------------------------------------------------------------
draw_terminal([
    ("=" * 52,                                                   GRAY),
    ("   Local Tone Rewriter (with voice)  -  llama3.2:3b",     WHITE),
    ("=" * 52,                                                   GRAY),
    ("",                                                          TEXT),
    ("Type your text, or type 'v' to speak it (or 'q' to quit):", TEXT),
    ("> i cant make it to the meeting tomorrow something came up", GREEN),
    ("",                                                          TEXT),
    ("Choose a tone:",                                            TEXT),
    ("  1. Professional",                                         CYAN),
    ("  2. Friendly",                                             TEXT),
    ("  3. Polite",                                               TEXT),
    ("  4. Confident",                                            TEXT),
    ("  5. Concise",                                              TEXT),
    ("  6. Funny",                                                TEXT),
    ("  7. Melancholic",                                          TEXT),
    ("> 1",                                                       GREEN),
    ("",                                                          TEXT),
    ("Rewriting in a Professional tone...",                       YELLOW),
    ("",                                                          TEXT),
    ("-" * 52,                                                   GRAY),
    ("Regrettably, I will be unable to attend the scheduled meeting tomorrow due to unforeseen circumstances.", WHITE),
    ("-" * 52,                                                   GRAY),
], title="Tone Rewriter  --  Professional", filename="01_professional.png")

# -----------------------------------------------------------------------
# Screenshot 2 - Funny tone
# -----------------------------------------------------------------------
draw_terminal([
    ("=" * 52,                                                   GRAY),
    ("   Local Tone Rewriter (with voice)  -  llama3.2:3b",     WHITE),
    ("=" * 52,                                                   GRAY),
    ("",                                                          TEXT),
    ("Type your text, or type 'v' to speak it (or 'q' to quit):", TEXT),
    ("> my code has a bug and I have no idea why",               GREEN),
    ("",                                                          TEXT),
    ("Choose a tone:",                                            TEXT),
    ("  1. Professional",                                         TEXT),
    ("  2. Friendly",                                             TEXT),
    ("  3. Polite",                                               TEXT),
    ("  4. Confident",                                            TEXT),
    ("  5. Concise",                                              TEXT),
    ("  6. Funny",                                                CYAN),
    ("  7. Melancholic",                                          TEXT),
    ("> 6",                                                       GREEN),
    ("",                                                          TEXT),
    ("Rewriting in a Funny tone...",                              YELLOW),
    ("",                                                          TEXT),
    ("-" * 52,                                                   GRAY),
    ("It sounds like your code is having an identity crisis - it's lost its way, and you're", WHITE),
    ("the only one who knows the password (i.e., the fix). Don't worry, we've all been there.", WHITE),
    ("Let's take a deep breath, grab some virtual coffee, and dive into troubleshooting mode!", WHITE),
    ("-" * 52,                                                   GRAY),
], title="Tone Rewriter  --  Funny", filename="02_funny.png")

# -----------------------------------------------------------------------
# Screenshot 3 - Voice input + Polite tone
# -----------------------------------------------------------------------
draw_terminal([
    ("=" * 52,                                                   GRAY),
    ("   Local Tone Rewriter (with voice)  -  llama3.2:3b",     WHITE),
    ("=" * 52,                                                   GRAY),
    ("",                                                          TEXT),
    ("Type your text, or type 'v' to speak it (or 'q' to quit):", TEXT),
    ("> v",                                                       GREEN),
    ("",                                                          TEXT),
    ("[mic] Listening... speak now.",                             BLUE),
    ("[mic] Processing...",                                       BLUE),
    ("[mic] You said: i need more time to finish this report",   BLUE),
    ("",                                                          TEXT),
    ("Choose a tone:",                                            TEXT),
    ("  1. Professional",                                         TEXT),
    ("  2. Friendly",                                             TEXT),
    ("  3. Polite",                                               CYAN),
    ("  4. Confident",                                            TEXT),
    ("  5. Concise",                                              TEXT),
    ("  6. Funny",                                                TEXT),
    ("  7. Melancholic",                                          TEXT),
    ("> 3",                                                       GREEN),
    ("",                                                          TEXT),
    ("Rewriting in a Polite tone...",                             YELLOW),
    ("",                                                          TEXT),
    ("-" * 52,                                                   GRAY),
    ("I'd be happy to help you extend the deadline for your report if needed.", WHITE),
    ("Would it be possible to discuss alternative dates that work better for you?", WHITE),
    ("-" * 52,                                                   GRAY),
], title="Tone Rewriter  --  Voice Input + Polite", filename="03_voice_polite.png")

print("\nDone. Screenshots saved to ./screenshots/")
