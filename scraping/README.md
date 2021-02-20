# minutes-scraper

## Purpose
Scrape all street names of Cambridge, MA from all minutes of City of Cambridge 

## How to use
1. Download all minutes
    1. Execute download_minutes.py at the root directory of this repository (minutes-scraper)
    1. The script makes pdf directory (minutes-scraper/pdf) first
    1. Download all minutes in the pdf directory
    1. Change each minute name [week], [month] [day], [year], [time] [name of meeting].pdf For example, FRIDAY, OCTOBER 2, 2020 11:00 AM Community Benefits Advisory Committee Regular Meeting.pdf 


2. Convert PDF to Text
    1. Please download pdfminer.six (https://github.com/pdfminer/pdfminer.six
) and put it the top directory of minutes-scraper
    1. Execute loop.sh at minutes-scraper/pdf directory
    1. The converted text file is saved in minutes-scraper/stat-finish/texted-pdf directory
    1. The file extention is changed from .pdf to .txt

3. Extract sentences with street names from the text file
    1. Execute word_process.py
    1. The extracted sentences is saved in minutes-scraper/stat-finish/region directory
    1. The word_process.py adds a prefix, "region-," to the output file name. The latter of the output file name is the same as the input file name.

4. Scrape street names from region files
    1. Execute classify_region.py
    1. The script reads a region file, and extract street names and context. 
        
        The script shows you each sentence line in the region file with contexts on the top screen.
       
        Then, the script shows all of the extracted street names on the bottom of screen.
        
        The below is an example of the output.
        ```
        --------------------------------------------
        sentence
        a lot of transparency on three sides; on the First Street side on Thorndike Way, and then on the Canal Park side… rusticated brick on the spandrels, and then up to the top of
        
        Pick up
        Canal Park side… rusticated 
        Reminders
        Park side… rusticated brick 
        Thorndike Way, and then 
        --------------------------------------------
        ```
        Context contains two types:
        
            1. Pick up 
                This type context are the street name which the script recognizes as a street name.
            1. Reminders
                This type context are the street name which the script cannot recognize as a street name.
                It might be street name or it might be different.
        
        The below is an example of the street names
        ```
        Ames Street
        Amherst Street
        Binney Street
        Broadway
        Cambridgeside Place
        Canal Park
        Dock Street
        Hayward Street
        Hurley Street
        Land Boulevard
        Main Street
        Memorial Drive
        Reed Street
        Vassar Street
        Wadsworth Street
        ```
        
    1. The script allows user to edit street_list.js and the extracted street names in runtime.
        
        The below is the commands
    
        ```
               n: Next file
               a: Add street name to street_list and parse again
               e: Edit street name
        any keys: Parse again the same file
        ```

            1. n: Next file
                Save the street name and scrape a next region file.
            2. a: Add street name to street_list and parse again
                Add street name in street_list.js and run the parser again.
                For example, the script fails to recognize Throndike Way as a street name in the below.
                If you add Thorndike Way to street_list.js, the script can recognize Thorndike Way as a street name.
                ```
                --------------------------------------------
                sentence
                a lot of transparency on three sides; on the First Street side on Thorndike Way, and then on the Canal Park side… rusticated brick on the spandrels, and then up to the top of
                
                Pick up
                Canal Park side… rusticated 
                Reminders
                Park side… rusticated brick 
                Thorndike Way, and then 
                --------------------------------------------
                ```
            3. e: Edit street name
                Right now, you can delete street names from the result on runtime.
                If you find alias street name, you can delete it.
                Also, the script recognizes false street names.
                Example:
                If a sentence contains Mount Auburn Street, it extracts Mount Auburn Street and Auburn Street.
                Mount Auburn Street and Auburn Street are legitimate street name in Cambridge.
               
      1. The script saves the result.
        
        If the user saves the result by entring the n command, the result is stored in memory.
        The script saves the data whenever finishes, even it stops working abruptly due to `CNTL-C` or other reasons.
        Therefore, the users do not worry about the data loss unless the computer is phisically broken.
        
