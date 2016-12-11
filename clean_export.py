# Clean
# 1. duplicate product entries
# 2. rows where High_res_img urls are empty
# 3. rows where High_res_img url are present but did not work, using image download logs
# 4. rows whose exact duplicate images already exist
# 5. rows for whom the text extraction url did not work (it will be cleaned while extracting the textual data)
# 6. Stopwords and punctuations removal from extracted text (it will be done after text extraction)

# columns : ['product_id' 'prod_id' 'Quality' 'URL' 'supplier_id' 'High_res_img' 'Low_res_img' 'Thumbnail_img' 'UNCATID'
#           'Category_ID' 'm_prod_id' 'ean_upcs' 'model_name' 'original_supplier_id' 'product_view' 'on_market'
#           'country_market_set' 'Updated']



import pickle
import sys
import pandas as pd
import os
from PIL import Image
#import imagehash # only in python 2.7, gives 32 bit hash values
import glob
import hashlib # gives 128 bit hash values

def main():

    data_path = sys.argv[1] #folder path for input data
    output_path = sys.argv[2] #folder path to store output files
    images_folder = sys.argv[3] # folder where downloaded images are kept

    input_file = data_path + "export_urls_rich.txt"
    image_download_log = output_path + "download_log_export.txt"
    output_file_df = output_path + "df_clean_export.p" # to store the dataframe obtained after CLEANING as pickle object

    df = pd.read_table(input_file, sep='\t', nrows = None) # reading first 10000 lines, to read whole file (nrows = None)
    print("Number of Data - begin {}".format(len(df)))
    df = df.drop_duplicates(subset=['product_id'], keep='first') # clean 1
    print("Number of Data after drop duplicate products {}".format(len(df)))
    df = df[pd.notnull(df['High_res_img'])] # clean 2
    print("Number of Data after clean empty High Res fields {}".format(len(df)))

    
# clean 3 - rows where High_res_img url are present but did not work, using image download logs

    download_log_df = pd.read_table(image_download_log, sep='\t', names = ['log'])
    s = download_log_df.ix[:,0]
    download_log_df = download_log_df[s.str.startswith('http')==True]
    download_log_df = pd.Series(download_log_df['log'])
    try:
        download_log_df = download_log_df.str.extract('([/])?(\d+)')
    except Exception:
        print("According to images download log, some urls don't have ([/])?(\d+) pattern")
        sys.exit()
    download_log_df = pd.to_numeric(download_log_df.ix[:,1])
    list_to_remove = download_log_df.tolist()
    list_to_remove = set(list_to_remove)

    df = df[~df['product_id'].isin(list_to_remove)] # clean 3
    print("Number of Data after remove failed entries in download log {}".format(len(df)))
    # few rows still remains which should be removed, like
    # 1. ids which were wrongly reported in log, like multiple ids have same image url (#63)
    # 2. ids reported but they do not exist in real dataset (#133)eg: product_id = 18328897


# clean 4 - rows whose exact duplicate images already exist
    hash_map = {}
    duplicate = []
    #images = os.listdir(images_folder)
    images = glob.glob(images_folder + '*.*')
    print("No. of images downloaded {}".format(len(images)))
    for path in images:
        #hash_value = imagehash.average_hash(Image.open(path))
        imagefile = open(path, "rb").read()
        hash_value = hashlib.md5(imagefile).hexdigest()
        try:
            pid = pd.to_numeric(pd.Series([path]).str.extract('([/])?(\d+)').ix[:,1])[0]
        except Exception:
            continue


        if hash_map.get(str(hash_value)) is None:
            hash_map[str(hash_value)] = pid
        else:
            duplicate.append(pid)

    print("Number of Duplicate images {}".format(len(duplicate)))

    df = df[~df['product_id'].isin(duplicate)] # clean 4
    print("Number of Data - end {}".format(len(df)))
    


 # Storing the dataframe obtained after cleaning, as pickle object
    with open(output_file_df, 'wb') as fp:
        pickle.dump(df, fp)

    '''
    # pickle file can be loaded from disk when required as follow
    with open(output_file_df, 'rb') as fp:
        df = pickle.load(fp)
    '''


if __name__ == '__main__':
    main()
