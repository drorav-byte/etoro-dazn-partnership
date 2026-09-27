from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "assets" / "dazn-germany-football-headpic.png"
target = ROOT / "assets" / "dazn-germany-football-headpic-native-1120x390.png"

with Image.open(source) as image:
    source_ratio = image.width / image.height
    target_ratio = 1120 / 390
    if source_ratio > target_ratio:
        crop_width = round(image.height * target_ratio)
        left = (image.width - crop_width) // 2
        box = (left, 0, left + crop_width, image.height)
    else:
        crop_height = round(image.width / target_ratio)
        top = (image.height - crop_height) // 2
        box = (0, top, image.width, top + crop_height)
    cropped = image.crop(box).resize((1120, 390), Image.Resampling.LANCZOS)
    cropped.save(target, format="PNG", optimize=True)
    print(f"{target} {cropped.width}x{cropped.height}")
