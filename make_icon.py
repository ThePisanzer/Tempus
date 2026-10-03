from PIL import Image, ImageDraw

BG = "#1a1a1a"
FG = "#e0e0e0"
ACCENT = "#0a84ff"
SIZE = 256


def draw_clock_icon(size):
    img = Image.new("RGBA", (size, size), BG)
    draw = ImageDraw.Draw(img)

    pad = size // 16
    draw.ellipse(
        [pad, pad, size - pad, size - pad],
        outline=FG, width=max(1, size // 64)
    )

    cx, cy = size // 2, size // 2
    r = size // 2 - pad - size // 16

    top = cy - r
    draw.line([cx, cy, cx, top], fill=ACCENT, width=max(2, size // 48))
    half_w = size // 10
    draw.line([cx - half_w, top, cx + half_w, top], fill=ACCENT, width=max(2, size // 48))

    right = cx + r
    draw.line([cx, cy, right, cy], fill=FG, width=max(2, size // 64))

    dot = size // 32
    draw.ellipse([cx - dot, cy - dot, cx + dot, cy + dot], fill=ACCENT)

    return img


def main():
    sizes = [16, 24, 32, 48, 64, 128, 256]
    base = draw_clock_icon(SIZE)
    base.save(
        "tempus_icon.ico",
        format="ICO",
        sizes=[(s, s) for s in sizes]
    )
    base.save("tempus_icon.png")
    print("已生成 tempus_icon.ico 和 tempus_icon.png")


if __name__ == "__main__":
    main()