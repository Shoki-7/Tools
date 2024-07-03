from pathlib import Path
from pdf2image import convert_from_path
import glob
import os

def pdf_image(pdf_file,img_path, fmt='png', dpi=200):

    #pdf_file、img_pathをPathにする
    pdf_path = Path(pdf_file)
    image_dir = Path(img_path)

    # PDFをImage に変換(pdf2imageの関数)
    pages = convert_from_path(pdf_path, dpi)

    # 画像ファイルを１ページずつ保存
    if len(pages) == 1:
        file_name = '{}.{}'.format(pdf_path.stem,fmt)
        image_path = image_dir / file_name
        pages[0].save(image_path, fmt)
    else:
        for i, page in enumerate(pages):
            file_name = '{}_{:02d}.{}'.format(pdf_path.stem,i+1,fmt)
            image_path = image_dir / file_name
            page.save(image_path, fmt)

if __name__ == "__main__":
    # PDFファイルのパス
    pdf_dir = input('Please input the directory path of PDF folders : ')
    pdf_files = glob.glob(os.path.join(pdf_dir, '*.pdf'))
    for pdf_file in pdf_files:
        pdf_image(pdf_file=pdf_file,img_path=pdf_dir, fmt='png', dpi=200)