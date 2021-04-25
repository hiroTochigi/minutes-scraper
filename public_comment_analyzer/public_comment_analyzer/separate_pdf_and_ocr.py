from PyPDF2 import PdfFileReader, PdfFileWriter

import extract_text_by_orc as ocr

def separate_page_list(pages):

    page_list = [ 
        ( start, start + 50 if (pages - start) > 50 else pages ) 
        for start in range(0, pages, 50) if start <= pages 
    ]
    return page_list

def separate_pdf_and_ocr(input, output):
    print(f"Separate {input} into several pdfs")
    with open(input, "rb") as infile:

        reader = PdfFileReader(infile)
        page_list = separate_page_list(reader.getNumPages())
        for index, page in enumerate(page_list):
            writer = PdfFileWriter()
            for i in range(page[0], page[1]):
                writer.addPage(reader.getPage(i))

            pdf_name = f"{input.split('/')[-1][:-4]}"
            new_input = f"separated_pdf/{pdf_name}-{index+1}.pdf"
            with open(new_input, 'wb') as outfile:
                writer.write(outfile)

            print(f"Ocr {new_input}")
            ocr.extract_text_by_orc(new_input, output, separated=True )

def main():
    example = "each_public_comment_pdf/COM 329 #2020.pdf"
    separate_pdf_and_store(example_input, 'separate_and_ocr_test.txt')

if __name__ == '__main__':
    main()