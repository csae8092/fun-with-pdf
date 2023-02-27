#Import required dependencies
import fitz
import glob
import shutil
import os
from tqdm import tqdm
from PIL import Image

SOURCE_DIR = "/home/csae8092/Documents/bv-play/"

files = sorted(glob.glob(f"{SOURCE_DIR}*.pdf"))
for x in tqdm(files, total=len(files)):
    new_folder = x.replace('.pdf', '')
    _, tail = os.path.split(x)
    shutil.rmtree(new_folder, ignore_errors=True)
    os.makedirs(new_folder)
    pdf_file = fitz.open(x)
    page_nums = len(pdf_file)
    images_list = []
    for page_num in range(page_nums):
        page_content = pdf_file[page_num]
        images_list.extend(page_content.get_images())
    for i, img in enumerate(images_list, start=1):
        xref = img[0]
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image['image']
        image_ext = base_image['ext']
        image_name = f"{tail.replace('.pdf', '')}__{i}.{image_ext}"
        with open(os.path.join(new_folder, image_name) , 'wb') as image_file:
            image_file.write(image_bytes)
            image_file.close()
    jpgs = sorted(glob.glob(f"{new_folder}/*.{image_ext}"))
    for jp in tqdm(jpgs, total=len(jpgs)):
        new_name = jp.replace('.jpeg', '.tif')
        im = Image.open(jp)
        im.save(new_name)
        os.remove(jp)