import matplotlib.pyplot as plt
import pandas as pd
import sys

FOLDER = sys.argv[1]
COLUMN = "High_res_img"
FOLDER_OUT = sys.argv[2]
CAT_FILE = "categorization_1.txt"
LIST_COLUMNS = ['product_id','High_res_img', 'Category_ID']
TARGET_FILE = "on_market.export_urls_rich.txt"

#TARGET_FILE = "daily.export_urls_rich.txt"
OUTPUT_FILE = "list_images.txt"

MOD_COL_NAME = 'catid'

df = pd.read_csv(FOLDER + TARGET_FILE, sep="\t")
df = df[LIST_COLUMNS][pd.notnull(df[COLUMN])]
df = df.drop_duplicates(subset=['product_id'], keep= 'first') # removing duplicate information of same product

df.rename(columns={'Category_ID': MOD_COL_NAME}, inplace=True)

cat_df = pd.read_csv(FOLDER + CAT_FILE, sep="\t")
cat_df.drop('uncatid', axis=1, inplace=True)
cat_df.loc[len(cat_df)] = [0, 'other']

print(df.head())

list_url = df[COLUMN]
list_url.to_csv(FOLDER_OUT + OUTPUT_FILE, index=False)
number_classes = len(df[MOD_COL_NAME].unique())

'''
Prune low frequency classes
'''
threshold = 20 # Min freq of items in a class for this class to be considered
value_counts = df[MOD_COL_NAME].value_counts()  # Specific column

to_remove = value_counts[value_counts <= threshold].index

pruned_df = df.copy()
pruned_df[MOD_COL_NAME].replace(to_remove, 0, inplace=True)

df = pd.merge(df, cat_df, how='left')
pruned_df = pd.merge(pruned_df, cat_df, how='left')

pruned_classes = len(pruned_df[MOD_COL_NAME].unique())

print("Number of images {}".format(list_url.size))
print("Number of classes {}".format(number_classes))
print("Number of classes after pruning {}".format(pruned_classes))
print(df['name'].value_counts(normalize=True)) # Relative classes distribution
print(pruned_df['name'].value_counts(normalize=True))
print(pruned_df['name'].value_counts().to_dict()['other']) # Number of items under "other"

plt.figure(1)
plt.subplot(211)
df[MOD_COL_NAME].hist(bins=number_classes)
plt.subplot(212)
pruned_df[MOD_COL_NAME].hist(bins=number_classes)

plt.savefig("distribution_full.png")
#plt.show()