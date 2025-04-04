import re
import unicodedata

### Data Cleaning and Normalisation of the text###

# Regex pattern to keep Bengali characters and whitespace
chars_to_ignore_regex = r'[^\u0980-\u09FF\s]'

def preprocess_bangla_fake_news(text):
    """
    Preprocess Bengali text for Fake News Detection using Bangla BERT.

    Steps:
    1. Convert to Unicode Normal Form (NFKC) for consistency.
    2. Replace numbers with a placeholder `<NUM>`.
    3. Remove special characters (except Bengali script, punctuation, and necessary symbols).
    4. Normalize multiple spaces.

    Args:
        text (str): The raw Bengali text.

    Returns:
        str: The preprocessed text.
    """
    # Convert to Unicode Normal Form (NFKC) for consistency
    text = re.sub(r'\s+', ' ', text.strip())  # Normalize spaces

    # Replace all numbers with <NUM>
    text = re.sub(r'\d+', '<NUM>', text)

    # Remove unnecessary special characters (preserve Bengali script and essential punctuation)
    text = re.sub(r'[^ঀ-৿a-zA-Z<>।,!?:;\-\–—\'"(){}\[\]]', ' ', text)

    # Normalize multiple spaces again
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def preprocess_bangla_text(text):
    # Normalize Unicode and remove unwanted characters
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(chars_to_ignore_regex, '', text)
    text = re.sub(r'[\u09E6-\u09EF]', '', text)  # Remove Bengali numbers
    text = text.lower()  # Convert to lowercase

    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def clean_api_texts(texts):
    """
        Cleans a list of text strings by removing:
          - HTML tags (e.g., <a>, <br>)
          - HTML entities (e.g., &amp;, &#39;)
          - URLs (starting with http, https, or www)
          - Timestamps (e.g., 7:52, 5:40)
          - Extra whitespace

        Args:
            texts (list): A list of text strings.

        Returns:
            list: A list of cleaned text strings.
        """
    cleaned_texts = []
    for text in texts:
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove HTML entities like &amp;, &#39;
        text = re.sub(r'&\w+;', '', text)
        # Remove URLs (starting with http, https, or www)
        text = re.sub(r'(http|https|www)\S+', '', text)
        # Remove timestamps in the form of "7:52" or "12:34"
        text = re.sub(r'\d{1,2}:\d{2}', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        cleaned_texts.append(text)
    return cleaned_texts

