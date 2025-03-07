from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import google.generativeai as genai
import json

model_path =  "C:\\Users\\dipsa\\Projects\\Social Media Comment Analysis\\backend\\models"
key_path = "C:\\Users\\dipsa\\Projects\\Social Media Comment Analysis\\backend\\api_keys.json"

def load_gemini_model(model_name: str = "gemini-1.5-flash"):
    # Load Google API Key
    with open(key_path) as f:
        api_keys = json.load(f)
    # Configure Gemini API
    genai.configure(api_key=api_keys["GOOGLE_API_KEY"])

    # Load the Gemini model
    gemini_model = genai.GenerativeModel(model_name)
    return gemini_model


def load_hate_classifier():
    # Load the model for Hate Speech Detection
    model_hate = AutoModelForSequenceClassification.from_pretrained(
        f"{model_path}\\hate_speech\\bangla-hate_speech-model")

    # Load the Tokenizer for Hate Speech Detection
    tokenizer_hate = AutoTokenizer.from_pretrained(
        f"{model_path}\\hate_speech\\bangla-hate_speech-model")

    # Create a pipeline for Hate Speech Analysis
    hate_classifier = pipeline("text-classification", model=model_hate, tokenizer=tokenizer_hate)

    return hate_classifier

def load_fake_classifier():
    ##Not Great (Unbalanced Data)--> Optional Use
    # Load the model for Fake News Detection
    model_fake = AutoModelForSequenceClassification.from_pretrained(
        f"{model_path}\\fake_news\\bangla_fake_news")

    # Load the Tokenizer for Fake News Detection
    tokenizer_fake = AutoTokenizer.from_pretrained(
        f"{model_path}\\fake_news\\bangla_fake_news")

    # Create a pipeline for Fake News Analysis
    fake_classifier = pipeline("text-classification", model=model_fake, tokenizer=tokenizer_fake)
    return fake_classifier


def load_sentiment_classifier():
    # Load the model for Sentiment Analysis
    model_sentiment = AutoModelForSequenceClassification.from_pretrained(
        f"{model_path}\\sentiment_analysis\\bangla-sentiment-model")

    # Load the Tokenizer for Sentiment Analysis
    tokenizer_sentiment = AutoTokenizer.from_pretrained(
        f"{model_path}\\sentiment_analysis\\bangla-sentiment-model")

    # Create a pipeline for Sentiment Analysis
    sentiment_classifier = pipeline("sentiment-analysis", model=model_sentiment, tokenizer=tokenizer_sentiment)

    return sentiment_classifier