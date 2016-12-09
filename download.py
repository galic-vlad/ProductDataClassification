import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib

# Downloading the dataset programatically from a URL.
def main():

    url = sys.argv[1] # icecat open dataset url
    user = sys.argv[2] # icecat username
    password = sys.argv[3] # icecat pwd
    path = sys.argv[4] # folder where files are saved

    page = requests.get(url, auth=(user, password))
    soup = BeautifulSoup(page.content, "lxml")

    for row in soup.find_all('a', href = True):
        fileurl = urljoin(url, row['href'])
        file =requests.get(fileurl, auth=(user, password))
        with open(path + row.get_text(), "wb") as code:
            code.write(file.content)

#urllib.urlretrieve('http://data.icecat.biz/export/freeurls/supplier_mapping.xml','./pdt')

if __name__ == '__main__':
    main()
