# Import libraries
from PIL import Image
from PIL import ImageOps
import pytesseract
import sys
from pdf2image import convert_from_path, convert_from_bytes
import os.path
import re
from collections import Counter
import cv2
import numpy as np
from pytesseract import Output
import csv
from pathlib import Path


def convert_pdf_to_image(path, final_name):
    converted_images = convert_from_path(child, 500)
    image_list =[]
    for image in converted_images:
        filename = final_name + ".jpg"
        image.save(filename, 'JPEG')
        image_list.append(filename)
    return image_list


def pre_processing_image(path):
    img = Image.open(path)
    open_cv_image = np.array(img)
    umat_image = cv2.UMat(open_cv_image)
    threshold = 120
    retval, img = cv2.threshold(umat_image, 12, threshold, 105, cv2.THRESH_BINARY)
    img = Image.fromarray(img.get())
    img.save(path)


def convert_to_text(path, final_name):
    no_crop_custom_oem_psm_config = r'--oem 1 --psm 6'
    text = str(pytesseract.image_to_string(Image.open(path), config=no_crop_custom_oem_psm_config))
    text = text.replace('-\n', '')

    with open(final_name +'.txt', "a+") as f:
        f.write(text)

def convert_text_to_csv(text_file):
    with open(text_file,'r') as infile:
        text=infile.read()

    purchase_order = re.findall(r'(?<=Purchase\sOrder\sNumber:\s)[0-9]{3}\D[0-9]{5}', text)
    carrier = re.findall(r'Ship Via:\s*(.*)', text, re.MULTILINE)
    tracking_number = re.findall(r'Tracking Number\s*(.*)', text, re.MULTILINE)

    data = [[purchase_order, carrier, tracking_number]]
    with open('San_Jamar_Spreadsheet.csv', 'a+') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    pass

def list_text_files(path):
    for file in os.listdir(path):
        if file.endswith(".txt"):
            print(os.path.join(path, file))

def get_text_files(path):
    files = []
    for file in os.listdir(path):
        if file.endswith('.txt'):
            files.append(os.path.join(path, file))
    return files





# Path of the pdf
my_path = os.path.abspath(os.path.dirname(__file__))

counter = 0
pages = []
path = Path('/Users/alexandrubordei/Library/Preferences/PyCharmCE2018.3/scratches')
p = Path('/Users/alexandrubordei/PycharmProjects/OCR/emails')

for child in p.iterdir():
    counter += 1
    output = "page_" + str(counter)
    final_name = output
    filepaths = convert_pdf_to_image(child, output)
    for filepath in filepaths:
        pre_processing_image(filepath)
        convert_to_text(filepath, final_name)

for text_file in get_text_files(path):
    convert_text_to_csv(text_file)
