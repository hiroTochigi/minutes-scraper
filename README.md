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


## Associate the street names to each minutes
I am developing a CLI tools.

The main problem is that it is hard to programmatically distinguish the street name is associated with the topic of the meeting or the street name is the resident address of the participant of the meeting. A human can easily solve it. Therefore, the tool assists the human in accomplishing these tasks.

There is one point to assist.
1. The tool prints the street name out in a different color.
