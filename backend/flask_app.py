from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.clean_text import preprocess_bangla_text, preprocess_bangla_fake_news
from backend.load_models import load_fake_classifier, load_hate_classifier, load_sentiment_classifier

app = Flask(__name__)
CORS(app)  # This will allow all domains by default
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Replace with your client URL

fake_classifier = load_fake_classifier()
hate_classifier = load_hate_classifier()
sentiment_classifier = load_sentiment_classifier()


"""
# URIs for different detect API
DETECT_HATE_URI = "http://127.0.0.1:5000/detect"
"""

@app.route('/')
def index():
    app.logger.info("Index page")
    return jsonify({"message": "Welcome to Social Media Comment Analysis App using Flask!"})

@app.route('/detect_hate', methods=['POST'])
def detect_hate():
    try:
        data = request.get_json()

        text = data['transcription']
        norm_text = preprocess_bangla_text(text)

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
        result = fake_classifier(norm_text)
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
        norm_text = preprocess_bangla_text(text)

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
