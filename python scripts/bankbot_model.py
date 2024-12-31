#import modelules
import nltk
import pickle
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import numpy as np
from preprocess import textPreprocess
from predict import prediction
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')

#Load data
data = pd.read_csv("intents.csv")
data.head()

#Text Preprocessing
train_trans = textPreprocess(data.patterns.values)

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(max_features=200)

# Fit and transform the documents
vectorizer.fit(train_trans)
tfidf_matrix = vectorizer.transform(train_trans)
train_features = tfidf_matrix.toarray()

#Label encoder
labelEncode = LabelEncoder().fit(data.tag.values)
label = labelEncode.transform(data.tag.values)
num_classes = len(data.tag.unique())
target =  tf.one_hot(label, depth=num_classes)

#Save the  TF-IDF vectorizer
with open("vectorizer.pkl", "wb") as file:
  pickle.dump(vectorizer, file)

#Save the Label Encoder
with open("labelencoder.pkl", "wb") as file:
  pickle.dump(labelEncode, file)

# Define the model architecture
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(train_features.shape[1],)))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

# Compile the model
optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_features, label, epochs=3000, batch_size=8)

#Save the Model
model.save("model.h5")

# Load the vectorizer
with open("vectorizer.pkl", "rb") as file:
  loaded_vectorizer = pickle.load(file)

#Save the Label Encoder
with open("labelencoder.pkl", "rb") as file:
  loaded_encoder = pickle.load(file)

#Inference
print(prediction(["can i open my bank account?"], model, loaded_vectorizer, loaded_encoder))
print(prediction(["Hi"], model, loaded_vectorizer, loaded_encoder))
print(prediction(["check account balance"], model, loaded_vectorizer, loaded_encoder))
print(prediction(["transfer money to my mom account"], model, loaded_vectorizer, loaded_encoder))
print(prediction(["I want to view transaction"], model, loaded_vectorizer, loaded_encoder))
print(prediction(["Thanks"], model, loaded_vectorizer, loaded_encoder))
print(prediction(["I want to pay bills"], model, loaded_vectorizer, loaded_encoder))
print(prediction(["Could you give me branch address?"], model, loaded_vectorizer, loaded_encoder))
print(prediction(["I lost my debit card"], model, loaded_vectorizer, loaded_encoder))
print(prediction(["Can FATCA status be updated later?"], model, loaded_vectorizer, loaded_encoder))
print(prediction(["pay to anand"], model, loaded_vectorizer, loaded_encoder))