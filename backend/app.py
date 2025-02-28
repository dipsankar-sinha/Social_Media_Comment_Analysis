from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.clean_text import clean_text, clean_text_fake
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import pickle

app = Flask(__name__)
CORS(app)  # This will allow all domains by default
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Replace with your client URL

# Load the model for Hate Speech Detection
with open("models/hate_speech/logistic_model_hate.pkl", "rb") as f:
    lr_model_hate = pickle.load(f)

# Load the TF-IDF Vectorizer for Hate Speech Detection
with open("models/hate_speech/tfidf_vectorizer_hate.pkl", "rb") as f:
    tfidf_vectorizer_hate = pickle.load(f)

# Load the model for Hate Speech Detection
model_hate = AutoModelForSequenceClassification.from_pretrained("models/hate_speech//bangla-hatespeech-model")

# Load the Tokenizer for Hate Speech Detection
tokenizer_ha = AutoTokenizer.from_pretrained("models/hate_speech/bangla-hatespeech-model")

##Not Great --> Optional Use
# Load the model for Fake News Detection
with open("models/fake_news/logistic_model_fake.pkl", "rb") as f:
    lr_model_fake = pickle.load(f)

# Load the TF-IDF Vectorizer for Fake News Detection
with open("models/fake_news/tfidf_vectorizer_fake.pkl", "rb") as f:
    tfidf_vectorizer_fake = pickle.load(f)

# Load the model for Sentiment Analysis
model_sentiment = AutoModelForSequenceClassification.from_pretrained("models/sentiment_analysis/bangla-sentiment-model")

# Load the Tokenizer for Sentiment Analysis
tokenizer_sentiment = AutoTokenizer.from_pretrained("models/sentiment_analysis/bangla-sentiment-model")

#Create a pipeline for Sentiment Analysis
classifier = pipeline("sentiment-analysis", model=model_sentiment, tokenizer=tokenizer_sentiment)



# URIs for different detect API
DETECT_HATE_URI = "http://127.0.0.1:5000/detect"


@app.route('/')
def index():
    app.logger.info("Index page")
    return jsonify({"message": "Welcome to Social Media Comment Analysis App!"})

@app.route('/detect_hate', methods=['POST'])
def detect_hate():
    try:
        data = request.get_json()

        text = data['transcription']
        norm_text = clean_text_hate(text)

        # Feature Extraction using TF-IDF vectorizer
        feature_text = tfidf_vectorizer_hate.transform([norm_text])

        # Prediction
        result = lr_model_hate.predict(feature_text)
        app.logger.info(result)

        return jsonify({"Hate": str(result[0])})
    except Exception as e:
        app.logger.error(e)
        return jsonify({"error": str(e)}), 500

@app.route('/detect_fake', methods=['POST'])
def detect_fake():
    try:
        data = request.get_json()

        text = data['transcription']
        norm_text = clean_text_fake(text)

        # Feature Extraction using TF-IDF vectorizer
        feature_text = tfidf_vectorizer_fake.transform([norm_text])

        #Prediction
        result = lr_model_fake.predict(feature_text)

        app.logger.info(result)
        return jsonify({"Fake": str(result[0])})
    except Exception as e:
        app.logger.error(e)
        return jsonify({"error": str(e)}), 500

@app.route('/detect_sentiment', methods=['POST'])
def detect_sentiment():
    try:
        data = request.get_json()

        text = data['transcription']
        norm_text = clean_text_sentiment(text)

        # 3. Use the pipeline for inference
        result = classifier(norm_text)
        app.logger.info(result)

        return jsonify({"Sentiment": result[0]['label'].split('_')[-1]})
    except Exception as e:
        app.logger.error(e)
        return jsonify({"error": str(e)}), 500

# Not ready yet
"""
@app.route('/process_input', methods=['POST'])
def process_input():
    # Check if the request contains JSON text input
    if request.is_json:
        transcription_json = request.get_json()
        response_detect = requests.post(DETECT_HATE_URI, json=transcription_json)
        return response_detect.json()

    # No valid input found
    return jsonify({'error': 'No valid input found'}), 400
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
