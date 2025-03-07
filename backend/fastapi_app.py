from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from backend.clean_text import preprocess_bangla_text, preprocess_bangla_fake_news
from backend.load_models import load_fake_classifier, load_hate_classifier, load_sentiment_classifier

import google.generativeai as genai
import json
import logging
import os

app = FastAPI()

#Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#Loading the classifiers for Hate Speech, Fake News and Sentiment Detection
fake_classifier = load_fake_classifier()
hate_classifier = load_hate_classifier()
sentiment_classifier = load_sentiment_classifier()


# Load Google API Key
with open("C:\\Users\\dipsa\\Projects\\Social Media Comment Analysis\\backend\\api_keys.json") as f:
    api_keys = json.load(f)

# Configure Gemini API
genai.configure(api_key=api_keys["GOOGLE_API_KEY"])

# Load the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Request type
class TextRequest(BaseModel):
    texts: list[str]

#Response type
class TextAnalysisFormat(BaseModel):
    original_text: str | None = None
    converted_text: str
    topic: str | None = None
    emotion: str | None = None
    spam: str | None = None
    hate: str | None = None
    sentiment: str | None = None
    fake: str | None = None
    
class TextResponse(BaseModel):
    results: list[TextAnalysisFormat]
    
@app.get('/')
def index():
    logger.info("Index page")
    logger.info(os.getcwd())
    return HTMLResponse(content="<h1>Welcome to Social Media Comment Analysis App using FASTAPI!</h1>")

#Calling Gemini API to handle English and Code_Switched or Romanized Bengali

@app.post('/analyze_texts_with_gemini', response_model=TextResponse)
def analyze_texts_with_gemini(request: TextRequest) -> TextResponse:
    prompt = f"""
        You are an advanced AI assistant specializing in **multilingual text analysis**. Your task is to process text inputs in **Bengali, English, or Romanized Bengali** while strictly ensuring smooth and accurate execution.

        ### **Instructions (Strictly Follow These Rules)**
        1. **Text Conversion:**
           - If the input is in **English**, **translate** it into **pure Bengali**.
           - If the input is in **Romanized Bengali**, **transliterate** it into **pure Bengali**.
           - If the input is already in **Bengali**, keep it unchanged.
           - **Ensure all output text is in Bengali**.
           - **If a proper Bengali translation is not possible, transliterate English words into Bengali instead of leaving them in English**.

        2. **Classification Tasks (After Bengali Conversion):**
           - **Topic Classification**: Politics, Sports, Entertainment, Technology, Business, Health, Education, Other.
           - **Emotion Detection**: Happy, Sad, Angry, Fearful, Surprised, Neutral.
           - **Spam Detection**: Spam or Not Spam.

        3. **Strict Output Format (JSON Only)**
           - **Return only JSON data. No extra text, explanations, or comments.**
           - **Ensure the JSON is fully valid and parseable.**
           - **Every input must appear in `original_text` and its converted form in `converted_text`.**
           - **All `converted_text` must be fully in Bengali (translated or transliterated).**

        ### **JSON Output Format (STRICTLY FOLLOW THIS)**
        ```json
        {{
          "results": [
            {{
              "original_text": "Original input text",
              "converted_text": "Pure Bengali version of the text",
              "topic": "Politics/Sports/Entertainment/Technology/Business/Health/Education/Other",
              "emotion": "Happy/Sad/Angry/Fearful/Surprised/Neutral",
              "spam": "Spam/Not Spam"
            }},
            ...
          ]
        }}
        ```

        4. **Rules to Ensure Smooth Execution:**
           - **Do NOT omit any inputs.** Every text in the list must be processed.
           - **Strictly return only JSON, no explanations, notes, or extra characters.**
           - **Ensure proper JSON formatting so it can be parsed without errors.**
           - **If a text is unclear, process it to the best of your ability rather than skipping it.**
           - **If a proper Bengali translation is not possible for an English word, transliterate it into Bengali.**

        **Here are the texts to analyze:**
        {json.dumps(request.texts, ensure_ascii=False)}
        """
    try:
        response = model.generate_content(prompt)

        # Extract JSON content by stripping any unintended characters
        json_start = response.text.find("{")
        json_end = response.text.rfind("}") + 1
        cleaned_json = response.text[json_start:json_end]
        results = json.loads(cleaned_json)  # Convert to dictionary

        return TextResponse (
            results=results["results"]
        )

    except Exception as e:
        logger.error('Error :' + str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/detect_hate', response_model=TextResponse)
def detect_hate(request: TextRequest | TextResponse) -> TextResponse:
    try:
        results = process_hate(request)
        return TextResponse(
            results = results
        )
    except Exception as e:
        logger.error('Error :'+ str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/detect_fake_news')
def detect_fake_news(request: TextRequest | TextResponse) -> TextResponse:
    try:
        results = process_fake_news(request)
        return TextResponse(
            results = results
        )
    except Exception as e:
        logger.error('Error :'+ str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/detect_sentiment')
def detect_sentiment(request: TextRequest | TextResponse) -> TextResponse:
    try:
        results = process_sentiment(request)
        return TextResponse(
            results = results
        )
    except Exception as e:
        logger.error('Error :'+ str(e))
        raise HTTPException(status_code=500, detail=str(e))


def process_hate(request : TextRequest | TextResponse) -> list[TextAnalysisFormat]:
    results = []
    if isinstance(request, TextRequest):
        for text in request.texts:
            normalized_text = preprocess_bangla_text(text)
            result = hate_classifier(normalized_text)
            logger.info(f"{text} -> [Hate: {str(result)}]")
            results.append(
                TextAnalysisFormat(
                    converted_text=text,
                    hate='Not Hate' if int(result[0]['label'].split('_')[-1]) == 0 else 'Hate'
                )
            )
    else:
        for entry in request.results:
            text = entry.converted_text
            normalized_text = preprocess_bangla_text(text)
            result = hate_classifier(normalized_text)
            logger.info(f"{text} -> [Hate: {str(result)}]")
            entry.hate = 'Not Hate' if int(result[0]['label'].split('_')[-1]) == 0 else 'Hate'
            results.append(entry)

    return results

def process_sentiment(request : TextRequest | TextResponse) -> list[TextAnalysisFormat]:
    results = []
    if isinstance(request, TextRequest):
        for text in request.texts:
            normalized_text = preprocess_bangla_text(text)
            result = sentiment_classifier(normalized_text)
            logger.info(f"{text} -> [Sentiment: {str(result)}]")
            results.append(
                TextAnalysisFormat(
                    converted_text=text,
                    sentiment='Negative' if int(result[0]['label'].split('_')[-1]) == 0 else 'Positive'
                )
            )
    else:
        for entry in request.results:
            text = entry.converted_text
            normalized_text = preprocess_bangla_text(text)
            result = sentiment_classifier(normalized_text)
            logger.info(f"{text} -> [Sentiment: {str(result)}]")
            entry.sentiment = 'Negative' if int(result[0]['label'].split('_')[-1]) == 0 else 'Positive'
            results.append(entry)
    return results

def process_fake_news(request : TextRequest | TextResponse) -> list[TextAnalysisFormat]:
    results = []
    if isinstance(request, TextRequest):
        for text in request.texts:
            normalized_text = preprocess_bangla_fake_news(text)
            result = fake_classifier(normalized_text)
            logger.info(f"{text} -> [Authentic: {str(result)}]")
            results.append(
                TextAnalysisFormat(
                    converted_text = text,
                    fake =  'Fake' if int(result[0]['label'].split('_')[-1]) == 0 else 'Not Fake'
                )
            )
        return results
    else:
        for entry in request.results:
            text = entry.converted_text
            normalized_text = preprocess_bangla_fake_news(text)
            result = fake_classifier(normalized_text)
            logger.info(f"{text} -> [Authentic: {str(result)}]")
            entry.fake = 'Fake' if int(result[0]['label'].split('_')[-1]) == 0 else 'Not Fake'
            results.append(entry)
        return results