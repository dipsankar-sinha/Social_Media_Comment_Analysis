from nltk.corpus import stopwords
from bangla_stemmer.stemmer.stemmer import BanglaStemmer
import re
import unicodedata
import nltk
import BnLemma as Lemma

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

### Data Cleaning and Normalisation of the text###

# Regex pattern to keep Bengali characters and whitespace
chars_to_ignore_regex = r'[^\u0980-\u09FF\s]'

def clean_text_fake(text):
    text = re.sub(r"http\S+|www\S+|@\S+|#", "", text)  # Remove URLs and mentions
    text = re.sub(r"[^A-Za-z\u0980-\u09FF ]", "", text)  # Keep Bengali & English alphabets
    return text.strip()

def clean_text(text):
    # Normalize Unicode and remove unwanted characters
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(chars_to_ignore_regex, '', text)
    text = re.sub(r'[\u09E6-\u09EF]', '', text)  # Remove Bengali numbers
    text = text.lower()  # Convert to lowercase

    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text