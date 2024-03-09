import os
import platform
import subprocess
import sys

import pdfkit
from pypdf import PdfWriter
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


ua = UserAgent()
session = requests.Session()

'''Settings'''
Url = ""
# Url should look like: https://servlib.com/harman-kardon/audio/esquire-mini.html

# First page to export
StartPage = 1
# Last page to export
EndPage = 9
# If the script should merge all pages into one single PDF
MakePdf = True
# Normally you don't need to change that, as it is the standard CSS that ServLib uses.
CssUrl = "https://servlib.com/templates/simple/css/template.css"
# Additional options for wkhtmltopdf
wkhtmltopdf_options = {
    'encoding': "UTF-8"
}


pdf_name = Url[Url.rfind("/") + 1: Url.rfind(".html")]

# wkhtmltopdf tool path selection
wkhtmltopdf_path = ""
if platform.system() == "Windows":
    if sys.maxsize > 2 ** 32:
        wkhtmltopdf_path = os.getcwd() + "/wkhtmltopdf/windows64/bin/wkhtmltopdf.exe"
    else:
        wkhtmltopdf_path = os.getcwd() + "/wkhtmltopdf/windows32/bin/wkhtmltopdf.exe"
else:
    try:
        devnull = open(os.devnull)
        subprocess.Popen(["wkhtmltopdf"], stdout=devnull, stderr=devnull).communicate()
        devnull.close()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print(
                "If you're on MAC or Linux you need to install the appropriete version of wkhtmltopdf for your system "
                "and add it to PATH from https://wkhtmltopdf.org/downloads.html")
            quit()

pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

# Create folder for tmp files
temp_path = os.getcwd() + "/tmp"
if not os.path.exists(temp_path):
    os.mkdir(temp_path)

# Save css styles
with open(temp_path + "/template.css", "w") as f:
    f.write(session.get(url=CssUrl, headers={"Host": "servlib.com", "User-Agent": ua.random}).text)
    f.close()

output_pdfs = []

for index in range(StartPage - 1, EndPage):
    print(f"Downloading page {index}")

    current_page_url = Url + f"?start={index}&limit=1"
    html = session.get(url=current_page_url, headers={"Host": "servlib.com", "User-Agent": ua.random}).text

    soup = BeautifulSoup(html, 'html.parser')
    pdf_page = str(soup.find("div", {"class": "pdfbg"}))
    # Correct link to be absolute, instead of relative to ServLib
    pdf_page = pdf_page[:pdf_page.find("url(") + 4] + "https://servlib.com" + pdf_page[pdf_page.find("url(") + 4:]
    # Center the background
    pdf_page = pdf_page[:pdf_page.find("no-repeat") + 9] + " center" + pdf_page[pdf_page.find("no-repeat") + 9:]

    output_pdf = temp_path + f"/page-{index}.pdf"
    output_pdfs.append(output_pdf)
    pdfkit.from_string(pdf_page, css=os.path.normpath(temp_path + "/template.css"),
                       output_path=output_pdf,
                       configuration=pdfkit_config, options=wkhtmltopdf_options)
    print(f"Page {index} successfully downloaded")

if MakePdf:
    print("\nMerging all PDFs")
    merger = PdfWriter()
    for pdf in output_pdfs:
        merger.append(pdf)
    merger.write(pdf_name + ".pdf")
    merger.close()
