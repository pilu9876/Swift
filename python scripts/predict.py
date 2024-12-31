from preprocess import textPreprocess
import numpy as np
import tensorflow
import tensorflow.keras.models as models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout


def prediction(x, model, loaded_vectorizer, loaded_encoder):
  x_arr = np.array(x)
  x_preprocess = textPreprocess(x_arr)
  test = loaded_vectorizer.transform(x_preprocess)
  y_pred = model.predict(test.toarray())
  label_pred = loaded_encoder.inverse_transform([np.argmax(y_pred)])
  return label_pred