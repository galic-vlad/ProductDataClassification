# This script uses on market dataset. For each product the working URL is visited and textual description of the product
# is extracted.A new column is added in the dataset with these extracted descriptions. The new dataset in the form of a dataframe
# is stored as a pickle object.

# The input for this file is the pickle object obtained after cleaning the on_market datadset.

import pickle
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import csv
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
from quantities import units



def bag_of_good_words(str):
    bow = [i for i in word_tokenize(str.lower()) if i not in stop and not i.isdigit() and i.isalpha()]
    return bow


def main():

    output_path = sys.argv[1] #folder path to store output files
    input_file_df = output_path + 'df_clean_on_market.p'
    output_file_pd = output_path + "Product_description_on_market.txt" # to store textual description for each product
    output_file_df = output_path + "df_text_extract_on_market.p" # to store the dataframe obtained after appending product description as pickle object
    URL = 'http://prf.icecat.biz/index.cgi?product_id='

    # Loading the pickle object which stores cleaned dataframe of on_market dataset
    with open(input_file_df, 'rb') as fp:
        df = pickle.load(fp)

    pid = df['product_id']

    # Extract URL of the product id, and get product description from there and store the descriptions
    desc =[]
    measuring_units = [u.symbol for _, u in units.__dict__.items() if isinstance(u, type(units.deg))]
    measuring_units = list(map(lambda x:x.lower(),measuring_units))
    others = ['height','width', 'depth', 'mah' , 'gb', 'inch', 'dpi', 'ppm','x', 'pixels', 'minute', 'second', 'hour']
    global stop
    stop = stopwords.words('english') + list(string.punctuation) + measuring_units + others

    with open(output_file_pd,'w') as fw:
        writer=csv.writer(fw, delimiter='\t',lineterminator='\n')
        for i in pid:
            url = URL + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "lxml")
            row = soup.find(name='div',attrs={"class":"text"})
            if row is None:
                df = df[df.product_id != i] # clean 5 - rows removal for whom the product url did not work
            else:
                texts = row.get_text().replace('More>>>','').replace('<<<Less','')
                texts = ' '.join(texts.split())
                bow = bag_of_good_words(texts) # clean 6 - Stopwords,punctuations,numbers, alphanumeric, units removal from extracted text
                writer.writerow([str(i),bow])
                fw.flush()
                desc.append(bow)

    df['desc'] = pd.Series(desc, index=df.index)


    # Storing the dataframe obtained after appending the description column, as pickle object
    with open(output_file_df, 'wb') as fp:
        pickle.dump(df, fp)


if __name__ == '__main__':
    main()
