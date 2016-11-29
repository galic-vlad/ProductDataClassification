from lxml import html
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd

def main():
    path = sys.argv[1] #filepath
    filename = path + "on_market.export_urls_rich.txt"

    df = pd.read_table(filename, sep='\t')
    df = df[pd.notnull(df['High_res_img'])]
    df = df.drop_duplicates(subset=['product_id'], keep='first')

    pid = df['product_id']

    # Extract URL of the product id, and get product description from there and store the descriptions
    with open('./Product_description.txt','w') as fw:
        for i in pid:
            url = 'http://prf.icecat.biz/index.cgi?product_id=' + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "lxml")
            for row in soup.find_all(name='div',attrs={"class":"text"}):
                texts = row.get_text().replace('More>>>','').replace('<<<Less','')
                fw.write(str(i))
                fw.write('\n')
                fw.write(' '.join(texts.split()))
                fw.write('\n')


if __name__ == '__main__':
    main()