from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from googleapiclient.discovery import build
import google.generativeai as gen_ai
import json

key_path = "./backend/api_keys.json"

def load_gemini_model(model_name: str = "gemini-1.5-flash"):
    # Load Google API Key
    with open(key_path) as f:
        api_keys = json.load(f)
    # Configure Gemini API
    gen_ai.configure(api_key=api_keys["GOOGLE_API_KEY"])

    # Load the Gemini model
    gemini_model = gen_ai.GenerativeModel(model_name)
    return gemini_model


def load_hate_classifier():
    # Load the model for Hate Speech Detection
    model_hate = AutoModelForSequenceClassification.from_pretrained(
        "./backend/models/hate_speech/bangla-hate_speech-model")

    # Load the Tokenizer for Hate Speech Detection
    tokenizer_hate = AutoTokenizer.from_pretrained(
        "./backend/models/hate_speech/bangla-hate_speech-model")

    # Create a pipeline for Hate Speech Analysis
    hate_classifier = pipeline("text-classification", model=model_hate, tokenizer=tokenizer_hate)

    return hate_classifier

def load_fake_classifier():
    ##Not Great (Unbalanced Data)--> Optional Use
    model_fake = AutoModelForSequenceClassification.from_pretrained(
        "./backend/models/fake_news/bangla-english_fake_news")

    # Load the Tokenizer for Fake News Detection
    tokenizer_fake = AutoTokenizer.from_pretrained(
        "./backend/models/fake_news/bangla-english_fake_news")

    # Create a pipeline for Fake News Analysis
    fake_classifier = pipeline("text-classification", model=model_fake, tokenizer=tokenizer_fake)
    return fake_classifier


def load_sentiment_classifier():
    # Load the model for Sentiment Analysis
    model_sentiment = AutoModelForSequenceClassification.from_pretrained(
        "./backend/models/sentiment_analysis/bangla-sentiment-model-v2")

    # Load the Tokenizer for Sentiment Analysis
    tokenizer_sentiment = AutoTokenizer.from_pretrained(
        "./backend/models/sentiment_analysis/bangla-sentiment-model-v2")

    # Create a pipeline for Sentiment Analysis
    sentiment_classifier = pipeline("sentiment-analysis", model=model_sentiment, tokenizer=tokenizer_sentiment)

    return sentiment_classifier

def load_youtube_v3():
    with open(key_path) as f:
        api_keys = json.load(f)
    youtube = build("youtube", "v3", developerKey=api_keys["YOUTUBE_API_KEY"])
    return youtube