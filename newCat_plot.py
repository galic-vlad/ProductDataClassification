import pandas as pd
import sys
import pickle
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def higherclass(depth,category_id):
	child = category_id
	for i in range(depth):
		if child_to_parent.get(child) is None:
			tag = soup.find("Category", ID=str(child))
			if tag is not None:
				parent_id = tag.find("ParentCategory").get('ID')
				child_to_parent[child] = int(parent_id)
			else:
				return category_id
		else:
			parent_id = str(child_to_parent[child])

		if parent_id == "1":
			return category_id

		child = int(parent_id)

	return parent_id



input_file_1 = "on_market.export_urls_rich.txt"
input_file_2 = "export_urls_rich.txt"
cat_xml = "categories.xml"

col = 'Category_ID'
fields = ['product_id','Category_ID','High_res_img']
df1 = pd.read_table(input_file_1, sep='\t',usecols=fields)
df2 = pd.read_table(input_file_2, sep='\t',usecols=fields)
df = pd.concat([df1, df2])
df = df.drop_duplicates(subset=['product_id'], keep='first') # clean 1
df = df[pd.notnull(df['High_res_img'])] # clean 2
unique_categories = df[col].unique()

print("Number of classes before setting new categories {}".format(len(unique_categories)))


global soup
soup = BeautifulSoup(open(cat_xml).read(), 'xml')
global child_to_parent 
child_to_parent = {}

old_to_new_cat = {}
count =1
for uc in unique_categories:
	hc = higherclass(depth=3, category_id=uc)
	old_to_new_cat[uc] = int(hc)
	#print("{}. {} => {}".format(count,uc,int(hc)))
	#count =count + 1


# Storing the dataframe obtained after cleaning, as pickle object
with open('old_to_new_category_mapping.p', 'wb') as fp:
	pickle.dump(old_to_new_cat, fp)


df1 = df.copy()
x = df1[col].replace(old_to_new_cat1)
df1 = pd.DataFrame(x, columns =[col])
number_classes_1 = len(df1[col].unique())
print("Number of classes after setting new category depth {}".format(number_classes_1))


plt.figure(1)
p1 = plt.subplot(211)
p1.set_title("Original Distribution")
df[col].hist(bins=len(unique_categories))
p2 = plt.subplot(212)
p2.set_title("Distribution @ depth 1")
df1[col].hist(bins=number_classes_1)


#plt.savefig("category_distribution_depth_1.png")
plt.show()

