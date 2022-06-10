import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# to download all, uncomment the below line
# nltk.download()

# Else,
nltk.download('wordnet')
nltk.download('stopwords')