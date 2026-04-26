from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ASSET = Path("assets/welcome.jpg")

def ensure_welcome_image():
    if ASSET.exists():
        return str(ASSET)
    ASSET.parent.mkdir(exist_ok=True)
    img = Image.new("RGB", (1280, 720), (12, 16, 33))
    draw = ImageDraw.Draw(img)
    for i in range(0, 1280, 8):
        color = (20 + i % 80, 70, 120 + i % 90)
        draw.line([(i, 0), (1280 - i // 2, 720)], fill=color, width=2)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle((90, 120, 1190, 600), radius=36, fill=(6, 10, 24, 185), outline=(88, 166, 255, 180), width=3)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB").filter(ImageFilter.SMOOTH)
    draw = ImageDraw.Draw(img)
    try:
        big = ImageFont.truetype("DejaVuSans-Bold.ttf", 72)
        small = ImageFont.truetype("DejaVuSans.ttf", 34)
    except Exception:
        big = small = None
    draw.text((150, 230), "Premium VC Music", fill=(238, 247, 255), font=big)
    draw.text((155, 335), "sᴛʀᴇᴀᴍ ʏᴏᴜᴛᴜʙᴇ & sᴘᴏᴛɪғʏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ", fill=(139, 220, 255), font=small)
    draw.text((155, 410), "/play <song name>", fill=(255, 232, 150), font=small)
    img.save(ASSET, quality=92)
    return str(ASSET)
