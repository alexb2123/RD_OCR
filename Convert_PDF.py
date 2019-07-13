#Import libraries
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os

#Path of the pdf
PDF_file = "/Users/alexandrubordei/PycharmProjects/OCR/ab_san_jamar.pdf"

'''
Part #1 : Converting PDF to images
'''

#store all the pages of the pdf in a variable
pages = convert_from_path(PDF_file, 600)

#counter to store images of each page of PDF to image
image_counter = 1

#iterate through all the pages stored above
for page in pages:

    #declaring filename for each page of pdf as jpg
    #for each page filename will be:
    #pdf page 1 -> page_1.jpg
    #pdf page 2 -> page_2.jpg
    #....
    filename = "page_"+str(image_counter)+".jpg"

    #save the image of the page in system
    page.save(filename, 'JPEG')

    # increment the counter to update filename
    image_counter = image_counter + 1


'''
Part #2 - Recognizing text from the images using OCR
'''


# Variable to get count of total number of pages
filelimit = image_counter-1

# Creating a text file to write the output
outfile = "out_text.txt"

# Open the file in append mode so that
# all contents of all images are added to the same file
f = open(outfile, "a")

# Iterate from 1 to total number of pages
for i in range(1, filelimit + 1):

    # set filename to recognize text from
    # again, these files will be:
    # page_1.jpg
    # page_2.jpg
    # ...
    filename = "page_"+str(i)+".jpg"

    #recognize the text as string in image
    text = str(((pytesseract.image_to_string(Image.open(filename)))))

    #the recognized text is stored in variable text
    #any string processing may be applied on text
    #here basic formating has been done:
    #in many pdfs, at line ending, if a word can't
    #be written full, a 'hyphen' is added
    #eg: this is a sample text this word here geeksf-
    #orgeeks is half on first line, remaining on next.
    #to remove this, we replace every '-\n' to ''.
    text = text.replace('-\n', '')

    #finally, write the processed text to the file
    f.write(text)

print(os.getcwd())