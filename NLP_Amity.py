import numpy as np
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
nltk.download('wordnet')
nltk.download('stopwords')
stopword=nltk.corpus.stopwords.words('english')
nltk.download('punkt')
from nltk.tokenize import word_tokenize


url="https://github.com/danmecj/WID3002-NLP-Assignment/raw/main/Extracted%20Reviews_V2.csv"
#Read Raw
df=pd.read_csv(url)



#Preprocessing
#Remove noise
df['Preprocessed']=df['text'].str.replace("@", "") 
df['Preprocessed']=df['text'].str.replace(r"http\S+", "") 
df['Preprocessed']=df['text'].str.replace("[^a-zA-Z]", " ")

def stopWord(text):
    preprocessWord=' '.join([i for i in text.split() if i not in stopword])
    return preprocessWord

df['Preprocessed']=df['Preprocessed'].apply(lambda text : stopWord(text.lower()))
df['Preprocessed']=df['Preprocessed'].apply(lambda text : nltk.word_tokenize(text))

lemmatizer = nltk.stem.WordNetLemmatizer()

def lemmatize_text(text):
    return [lemmatizer.lemmatize(i) for i in text]

df['Preprocessed']=df['Preprocessed'].apply(lambda text : lemmatize_text(text))

column=['Unnamed:','name','address','rating','text']
selectlist=[x for x in df.columns if x not in column]
datatowrite=df[selectlist]

datatowrite.to_csv('Preprocessed_Text.csv', encoding='utf-8',index=False)
