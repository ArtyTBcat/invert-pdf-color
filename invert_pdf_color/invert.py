from pdf2image import convert_from_path, convert_from_bytes

from pdf2image.exceptions import (
        PDFInfoNotInstalledError,
        PDFPageCountError,
        PDFSyntaxError
)

from PIL import Image, ImageOps
import os, fitz, cv2
import matplotlib.pyplot as plt
from fpdf import FPDF
from tqdm import tqdm


bin_root_path = os.path.join(os.getcwd())


def convert_a4_images_to_pdf(image_paths, output_pdf):
    A4_WIDTH, A4_HEIGHT = 210, 297
    pdf = FPDF('P', 'mm', 'A4')

    for image_path in tqdm(image_paths):
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        image_ratio = image.width / image.height
        a4_ratio = A4_WIDTH / A4_HEIGHT

        if image_ratio > a4_ratio:
            new_width = A4_WIDTH
            new_height = A4_WIDTH / image_ratio
        else:
            new_height = A4_HEIGHT
            new_width = A4_HEIGHT * image_ratio

        resized_image = image.resize((int(new_width * 3.7795275591), int(new_height * 3.7795275591)))  # Convert mm to pixels (1 mm = 3.7795275591 pixels)

        temp_image_path = os.path.join("bin", f"temp_image_{os.path.basename(image_path)}")
        resized_image.save(temp_image_path)
        pdf.add_page()
        pdf.image(temp_image_path, x=0, y=0, w=A4_WIDTH, h=A4_HEIGHT)
        os.remove(temp_image_path)
    pdf.output(output_pdf)





def invert_color(filepath:str):
    if not os.path.exists(os.path.join(os.getcwd(), 'bin')):
        os.makedirs(os.path.join(os.getcwd(), 'bin'))

    saved_images: list = []

    pdf_document = fitz.open(filepath)
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        save_path = os.path.join(bin_root_path, 'bin', f"_idx_{page_num}.png")
        pix.save(save_path)
        saved_images.append(save_path)
    pdf_document.close()

    for saved_image_path in saved_images:
        img = cv2.imread(saved_image_path)
        img = cv2.absdiff(img, 255)
        cv2.imwrite(saved_image_path, img)


    convert_a4_images_to_pdf(saved_images, (filepath.replace('.pdf', '') + '_inverted' + 
                                            '.pdf'))
    

    for toberemove in saved_images:
        os.remove(toberemove)

