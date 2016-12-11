import pickle
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd


# Loading the pickle object which stores cleaned dataframe of on_market dataset
with open('/home/rohit/Studies/Thesis/ProductDataClassification/output/df_product_desc.p', 'rb') as fp:
	df = pickle.load(fp)

pid = df['product_id'] #Series

#Random Samples for Training
pid_train = random.sample(list(pid),100000)
pid_test = random.sample(list(pid),10)

df_train = df[df['product_id'].isin(pid_train)]
df_test = df[df['product_id'].isin(pid_test)]
#print(df_train)

# Setting up Bag of Words Model
count_vect = CountVectorizer()
desc_train = df_train['desc']
X_train_counts = count_vect.fit_transform(list(desc_train))
print(X_train_counts.shape)
print(count_vect.vocabulary_.get('images'))

# Fitting tdidf vectorization
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# applying Multinominal Classifier on feature vectors obtained
clf = MultinomialNB().fit(X_train_tfidf, list(df_train['Category_ID']))


# testing the model, we only need transform as for the corpus the global weights of each term are alreday learned are already learned
desc_test = df_test['desc']
pid_test = df_test['product_id']
X_test_counts = count_vect.transform(list(desc_test))
X_test_tfidf = tfidf_transformer.transform(X_test_counts)

predicted = clf.predict(X_test_tfidf)

for i, category in zip(pid_test, predicted):
	print("{} => {}".format(i, category))














