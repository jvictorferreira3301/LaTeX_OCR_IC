import os
from pathlib import Path
from wand.image import Image
from wand.color import Color
from concurrent.futures import ThreadPoolExecutor

SRC_PATH = 'outputs/pdfs'
TRG_PATH = 'outputs/images'
RESOLUTION = 200  # lower resolution for faster processing

def convert_pdf_to_png(pdf_path):
    output_path = Path(TRG_PATH) / f"{pdf_path.stem}.png"
    with Image(filename=str(pdf_path), resolution=RESOLUTION) as img:
        img.format = 'png'
        img.depth = 8
        img.trim(color=Color('rgba(0,0,0,0)'), fuzz=0)  # Trim transparent areas
        img.background_color = Color('white')  # Set white background
        img.alpha_channel = 'remove'           # Remove transparency
        img.save(filename=str(output_path))
    print(f"Converted {pdf_path} to {output_path}")

def main():
    if not os.path.exists('outputs/images'):
        os.mkdir('outputs/images')

    pdf_dir = Path(SRC_PATH)
    pdf_files = list(pdf_dir.glob('*.pdf'))

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(convert_pdf_to_png, pdf_files)

if __name__ == "__main__":
    main()