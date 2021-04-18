import logging
import os
import sys
import traceback

from PIL import Image
import pytesseract
from pdf2image import convert_from_path

def log_traceback(ex, ex_traceback, input_file):
    tb_lines = traceback.format_exception(ex.__class__, ex, ex_traceback)
    tb_text = ''.join(tb_lines)
    logging.error(input_file)
    logging.error(tb_text)

def extract_text_by_orc(input, output):
    
    '''
    Part #1 : Converting PDF to images
    '''
    
    # Store all the pages of the PDF in a variable
    try:
        pages = convert_from_path(input, 500)
        
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
            filename = "jpg/page_"+str(image_counter)+".jpg"
            
            # Save the image of the page in system
            page.save(filename, 'JPEG')
        
            # Increment the counter to update filename
            image_counter = image_counter + 1
        
        '''
        Part #2 - Recognizing text from the images using OCR
        '''
        # Variable to get count of total number of pages
        filelimit = image_counter-1
        
        # Open the file in append mode so that 
        # All contents of all images are added to the same file
        f = open(output, "w")
        
        # Iterate from 1 to total number of pages
        for i in range(1, filelimit + 1):
        
            # Set filename to recognize text from
            # Again, these files will be:
            # page_1.jpg
            # page_2.jpg
            # ....
            # page_n.jpg
            filename = "jpg/page_"+str(i)+".jpg"
                
            # Recognize the text as string in image using pytesserct
            text = str(((pytesseract.image_to_string(Image.open(filename)))))
        
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
            f.write(text)
        
        # Close the file after writing all the text.
        f.close()

    except Exception as ex:
        _, _, ex_traceback = sys.exc_info()
        log_traceback(ex, ex_traceback, input)
