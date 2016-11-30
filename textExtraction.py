import pickle
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd

def main():
    data_path = sys.argv[1] #folder path for input data
    output_path = sys.argv[2] #folder path to store output files

    input_file = data_path + "on_market.export_urls_rich.txt"
    output_file_pd = output_path + "Product_description.txt" # to store textual description for each product
    output_file_df = output_path + "df_product_desc.p" # to store the dataframe obtained after appending product description as pickle object


    df = pd.read_table(input_file, sep='\t', nrows = 1000) # reading first 10000 lines, to read whole file (nrows = None)
    df = df[pd.notnull(df['High_res_img'])]
    df = df.drop_duplicates(subset=['product_id'], keep='first')

    pid = df['product_id']

    # Extract URL of the product id, and get product description from there and store the descriptions
    desc =[]
    with open(output_file_pd,'w') as fw:
        for i in pid:
            url = 'http://prf.icecat.biz/index.cgi?product_id=' + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "lxml")
            row = soup.find(name='div',attrs={"class":"text"})
            if row is None:
                df = df[df.product_id != i]
            else:
                texts = row.get_text().replace('More>>>','').replace('<<<Less','')
                texts = ' '.join(texts.split())
                fw.write(str(i))
                fw.write('\n')
                fw.write(texts)
                fw.write('\n')
                desc.append(texts)

    df['desc'] = pd.Series(desc, index=df.index)

    # Storing the dataframe obtained after appending the description column, as pickle object
    with open(output_file_df, 'wb') as fp:
        pickle.dump(df, fp)

    '''
    # pickle file can be loaded from disk when required as follow
    with open(output_file_df, 'rb') as fp:
        df = pickle.load(fp)
    '''

if __name__ == '__main__':
    main()