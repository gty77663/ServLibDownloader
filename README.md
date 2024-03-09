# ServLibDownloader - Download manuals into local and convert them to PDF

Access the manuals from [ServLib](https://servlib.com).
This for educational purposes on how to find and archive data. The project is inspired by [this](https://github.com/AriZoneVibes/ServLibScrapper/) repository 
from [AriZoneVibes](https://github.com/AriZoneVibes) with similar functionality, but improved to be able to parse PDFs with selectable text.

## Requirements

You will need to have [python](https://docs.microsoft.com/en-us/windows/python/beginners) installed on your computer.

Once installed, you can install everything you need by running this command either in venv, or in global python interpreter:  

```py
pip install -r requirements. txt
```

To generate PDFs from HTML wkhtmltopdf is used, for Windows it is already included in repository, 
but for Linux or Mac you need to install it yourself from [this website](https://wkhtmltopdf.org/downloads.html) and add it to PATH.

## Obtaining the link

The link required is the link to the main html page of the manual, which should look like this:  
`https://servlib.com/harman-kardon/audio/esquire-mini.html`

## Script

Open `Scrapper.py` file in your favorite text editor. Modify the settings according to the pages you need and if it should make a PDF file from all the pages.

```py
'''Settings'''
Url = ""
# Url should look like: https://servlib.com/harman-kardon/audio/esquire-mini.html

# First page to export
StartPage = 1  
# Last page to export
EndPage = 17  
# If the script should merge all pages into one single PDF
MakePdf = True  
# Normally you don't need to change that, as it is the standard CSS that ServLib uses.  
CssUrl = "https://servlib.com/templates/simple/css/template.css"  
# Additional options for wkhtmltopdf 
wkhtmltopdf_options = {
    'encoding': "UTF-8"
}
```

Save the file and open a terminal in the location where you want your files stored. Lastly, run the script. Will display the progress as the images are downloaded.

```powershell
python3 Scrapper.py
```

If you want to learn more about how the script works you can find information on the comments inside the `Scrapper.py` file
