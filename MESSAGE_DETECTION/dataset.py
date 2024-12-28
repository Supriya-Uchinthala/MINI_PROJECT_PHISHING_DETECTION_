import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import string
import pickle

# Load dataset
data = pd.read_csv('D:\\MINI-PROJECT\\spam-email-classifier\\data\\spam.tsv', sep='\t')

# Data cleaning and preprocessing
data1 = data.drop(['length', 'punct'], axis=1)
data1['label'] = data['label'].map({'ham': 1, 'spam': 0})
data1['text-clean'] = data1['message'].apply(
    lambda x: "".join([char for char in x if char not in string.punctuation])
)

# Splitting features and labels
X = data1['text-clean']
y = data1['label']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=10)

# Convert text to numerical data using CountVectorizer
cv = CountVectorizer(stop_words="english")
X_train_cv = cv.fit_transform(X_train)
X_test_cv = cv.transform(X_test)

# Train an SVM classifier
model_svm = SVC(kernel='linear', C=1, probability=True)
model_svm.fit(X_train_cv, y_train)

# Evaluate the model
y_pred = model_svm.predict(X_test_cv)
print(classification_report(y_test, y_pred))

# User input prediction
msg = input("Enter a message: ")
msg_input = cv.transform([msg])
predict = model_svm.predict(msg_input)
if predict[0] == 0:
    print('Spam')
else:
    print('Ham')

# TFIDF Vectorizer
tf = TfidfVectorizer(stop_words="english")
X_tf = tf.fit_transform(X)

# Split TFIDF data
X_train_tf, X_test_tf, y_train_tf, y_test_tf = train_test_split(X_tf, y, test_size=0.20, random_state=10)

# Train an SVM classifier with TFIDF
model_svm_tfidf = SVC(kernel='linear', C=1, probability=True)
model_svm_tfidf.fit(X_train_tf, y_train_tf)

# Evaluate the model with TFIDF
y_pred_tf = model_svm_tfidf.predict(X_test_tf)
print(classification_report(y_test_tf, y_pred_tf))

# Save the model and vectorizer using Pickle
with open('model_svm.pkl', 'wb') as f:
    pickle.dump((model_svm, cv), f)

# Save the TFIDF model and vectorizer
with open('model_svm_tfidf.pkl', 'wb') as f:
    pickle.dump((model_svm_tfidf, tf), f)
