import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
def textPreprocess(textList):

  #Lowering the data
  textLower = [text.lower() for text in textList]

  #Remove Special Character
  textRemSpe = [re.sub('[^a-zA-Z]+', ' ', text) for text in textLower]

  #Word Tokenize
  textToken = [word_tokenize(text) for text in textRemSpe]

  #Remove Stop word
  stop_words = list(set(stopwords.words('english')) - {'not', 'no', 'to'})
  textRemStop = []
  for text in textToken:
    textRemStop.append([word for word in text if word not in stop_words])

  #Stemming
  ps = PorterStemmer()
  textStem = []
  for text in textRemStop:
    textStem.append([ps.stem(word) for word in text])

  #Joining the words
  finalText = []
  finalText.extend([' '.join(text) for text in textStem])
  return finalText