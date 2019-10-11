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
import pprint




# Path of the pdf
my_path = os.path.abspath(os.path.dirname(__file__))
PDF_file = os.path.join(my_path, "S1968946-2.PDF")

if os.path.exists(PDF_file):
    pass
if not os.path.exists(PDF_file):
    print('PDF_file does not exist !')


'''
Part #1 : Converting PDF to images 
'''

pages = convert_from_path(PDF_file, 500)

# Counter to store images of each page of PDF to image
image_counter = 1

# Iterate through all the pages stored above
for page in pages:
    # Declaring filename for each page of PDF as JPG
    # For each page, filename will be:
    # PDF page 1 -> page_1.jpg
    # PDF page 2 -> page_2.jpg
    # PDF page 3 -> page_3.jpg
    # ....
    # PDF page n -> page_n.jpg
    filename = "page_" + str(image_counter) + ".jpg"

    # Save the image of the page in system
    page.save(filename, 'JPEG')

    # Increment the counter to update filename
    image_counter = image_counter + 1

#crop images
    image_to_crop = Image.open(filename)
    croppedIm = image_to_crop.crop((2233, 1276, 4015, 2123))
    croppedIm.save('cropped.jpg')


'''
Part #2 - Recognizing text from the images using OCR 
'''

# Variable to get count of total number of pages
filelimit = image_counter - 1

# Creating a text file to write the output
outfile = "out_text.txt"

# Open the file in append mode so that
# All contents of all images are added to the same file
f = open(outfile, "a+")

#config for pytesseract accuracy
custom_oem_psm_config = r'--oem 1--psm 6'


# Iterate from 1 to total number of pages
for i in range(1, filelimit + 1):
    # Set filename to recognize text from
    # Again, these files will be:
    # page_1.jpg
    # page_2.jpg
    # ....
    # page_n.jpg
    filename = "page_" + str(i) + ".jpg"


#Top left = 438, 258
#bottom right = 806,344


#create bounding boxes
#    image = cv2.imread(filename)
#    box = pytesseract.image_to_data(filename, output_type=Output.DICT)
#    n_boxes = len(box['level'])
#    for i in range(n_boxes):
#        (x, y, w, h) = (box['left'][i], box['top'][i], box['width'][i], box['height'][i])
#        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

#    cv2.imshow('img', image)
#    cv2.waitKey(0)

# pre-process image
    img = Image.open(filename)
    open_cv_image = np.array(img)
    umat_image = cv2.UMat(open_cv_image)
    threshold = 120
    retval, img = cv2.threshold(umat_image, 12, threshold, 105, cv2.THRESH_BINARY)
    img = Image.fromarray(img.get())
    img.save(filename)


# Recognize the text as string in image using pytesseract
    text = str(pytesseract.image_to_string(Image.open(filename), config=custom_oem_psm_config))

# The recognized text is stored in variable text
# Any string processing may be applied on text
# Here, basic formatting has been done:
# In many PDFs, at line ending, if a word can't
# be written fully, a 'hyphen' is added.
# The rest of the word is written in the next line
# Eg: This is a sample text this word here GeeksF-
# orGeeks is half on first line, remaining on next.
# To remove this, we replace every '-\n' to ''.
    text = text.replace('-\n', '')

# Finally, write the processed text to the file.
#    f.write(text)

#    text = str(pytesseract.image_to_string(croppedIm, config=custom_oem_psm_config))

#    text = text.replace('-\n', '')

    f.write(text)
# Look back at start of file
f.seek(0)

#box = pytesseract.image_to_boxes(Image.open(filename), output_type=Output.DICT)



#Find the PO Number
#Purchase Order Number
strings = re.findall(r'(?<=Purchase\sOrder\sNumber:\s)[0-9]{3}\D[0-9]{5}', text)
carrier = re.findall(r'Ship Via:\s*(.*)', text, re.MULTILINE)
tracking_number = re.findall(r'Tracking Number\s*(.*)', text, re.MULTILINE)


print(strings)
print(carrier)
print(tracking_number)
#pprint.pprint(box)
#print(box)

##Make sure PO nummber is not duplicated
#def not_singles(strings):
#    return [key for key, value in Counter(strings).items()
#            if value > 1]


#print(strings)
#a = not_singles(strings)

#print(a)

f.close()
