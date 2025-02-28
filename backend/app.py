from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.clean_text import clean_text, preprocess_bangla_fake_news
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import pickle

app = Flask(__name__)
CORS(app)  # This will allow all domains by default
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Replace with your client URL


# Load the model for Hate Speech Detection
model_hate = AutoModelForSequenceClassification.from_pretrained("models/hate_speech/bangla-hate_speech-model", )

# Load the Tokenizer for Hate Speech Detection
tokenizer_hate = AutoTokenizer.from_pretrained("models/hate_speech/bangla-hate_speech-model")

##Not Great (Unbalanced Data)--> Optional Use
# Load the model for Fake News Detection
model_fake = AutoModelForSequenceClassification.from_pretrained("models/fake_news/bangla_fake_news", )

# Load the Tokenizer for Fake News Detection
tokenizer_fake = AutoTokenizer.from_pretrained("models/fake_news/bangla_fake_news")

# Load the model for Sentiment Analysis
model_sentiment = AutoModelForSequenceClassification.from_pretrained("models/sentiment_analysis/bangla-sentiment-model")

# Load the Tokenizer for Sentiment Analysis
tokenizer_sentiment = AutoTokenizer.from_pretrained("models/sentiment_analysis/bangla-sentiment-model")


#Create a pipeline for Fake News Analysis
fake_classifier = pipeline("text-classification", model=model_fake, tokenizer=tokenizer_fake)

#Create a pipeline for Hate Speech Analysis
hate_classifier = pipeline("text-classification", model=model_hate, tokenizer=tokenizer_hate)

#Create a pipeline for Sentiment Analysis
sentiment_classifier = pipeline("sentiment-analysis", model=model_sentiment, tokenizer=tokenizer_sentiment)

"""
# URIs for different detect API
DETECT_HATE_URI = "http://127.0.0.1:5000/detect"
"""

@app.route('/')
def index():
    app.logger.info("Index page")
    return jsonify({"message": "Welcome to Social Media Comment Analysis App!"})

@app.route('/detect_hate', methods=['POST'])
def detect_hate():
    try:
        data = request.get_json()

        text = data['transcription']
        norm_text = clean_text(text)

        # Use the pipeline for inference
        result = hate_classifier(norm_text)
        app.logger.info("Hate: " + str(result))

        return jsonify({"Hate": result[0]['label'].split('_')[-1]})

    except Exception as e:
        app.logger.error("error: " + str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/detect_fake', methods=['POST'])
def detect_fake():
    try:
        data = request.get_json()

        text = data['transcription']
        norm_text = preprocess_bangla_fake_news(text)

        # Use the pipeline for inference
        result = hate_classifier(norm_text)
        app.logger.info("Authentic: " + str(result))

        return jsonify({"Authentic": result[0]['label'].split('_')[-1]})
    except Exception as e:
        app.logger.error(e)
        return jsonify({"error": str(e)}), 500

@app.route('/detect_sentiment', methods=['POST'])
def detect_sentiment():
    try:
        data = request.get_json()

        text = data['transcription']
        norm_text = clean_text(text)

        # Use the pipeline for inference
        result = sentiment_classifier(norm_text)
        app.logger.info("Sentiment: " + str(result))

        return jsonify({"Sentiment": result[0]['label'].split('_')[-1]})
    except Exception as e:
        app.logger.error("Error: "+ str(e))
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
