from pathlib import Path
from zipfile import ZipFile
from PIL import Image, ImageDraw

out = Path('demo.cbz')
with ZipFile(out, 'w') as zf:
    for i in range(1, 4):
        img = Image.new('RGB', (900, 1300), 'white')
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((120, 90, 650, 230), radius=40, outline='black', width=4)
        draw.text((160, 140), f'Demo page {i}: hello manga translator', fill='black')
        img_path = Path(f'{i:03d}.jpg')
        img.save(img_path, quality=95)
        zf.write(img_path, img_path.name)
        img_path.unlink()
print(out.resolve())
