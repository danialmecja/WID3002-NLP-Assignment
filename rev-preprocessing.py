# Imports
import numpy as np
import pandas as pd
import nltk

from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
stopword=nltk.corpus.stopwords.words('english')

# Pandas
df = pd.read_csv("Extracted Reviews_V2.csv")
#Remove noise
df['Preprocessed']=df['text'].str.replace("@", "") 
df['Preprocessed']=df['text'].str.replace(r"http\S+", "") 
df['Preprocessed']=df['text'].str.replace("[^a-zA-Z]", " ")
print(df)