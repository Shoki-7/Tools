from pathlib import Path
from pdf2image import convert_from_path
import glob
import os

def pdf_image(pdf_file, img_path, fmt='png', dpi=200):
    pdf_path = Path(pdf_file)
    image_dir = Path(img_path)

    # Ensure the output directory exists
    image_dir.mkdir(parents=True, exist_ok=True)

    # Convert PDF to Image using pdf2image
    pages = convert_from_path(str(pdf_path), dpi)

    # Save each page as an image file
    if len(pages) == 1:
        file_name = f'{pdf_path.stem}.{fmt}'
        image_path = image_dir / file_name
        pages[0].save(str(image_path), fmt)
    else:
        for i, page in enumerate(pages):
            file_name = f'{pdf_path.stem}_{i+1:02d}.{fmt}'
            image_path = image_dir / file_name
            page.save(str(image_path), fmt)

if __name__ == "__main__":
    # PDF directory path input
    pdf_dir = input('Please input the directory path of PDF folders: ')
    pdf_files = glob.glob(os.path.join(pdf_dir, '*.pdf'))
    
    for pdf_file in pdf_files:
        pdf_image(pdf_file=pdf_file, img_path=pdf_dir, fmt='png', dpi=200)
