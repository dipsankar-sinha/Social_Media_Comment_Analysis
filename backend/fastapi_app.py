from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from backend.clean_text import preprocess_bangla_text, preprocess_bangla_fake_news
from backend.load_models import load_fake_classifier, load_hate_classifier, load_sentiment_classifier
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

# Request type model
class Request(BaseModel):
    text: str

@app.get('/')
def index():
    logger.info("Index page")
    logger.info(os.getcwd())
    return HTMLResponse(content="<h1>Welcome to Social Media Comment Analysis App using FASTAPI!</h1>")
@app.post('/detect_hate')
def detect_hate(request: Request):
    try:
        result = []
        normalized_text = preprocess_bangla_text(request.text)
        result = hate_classifier(normalized_text)
        logger.info("Hate: " + str(result))
        return JSONResponse(content={"Hate": result[0]['label'].split('_')[-1]})
    except Exception as e:
        logger.error('Error :'+ str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/detect_fake')
def detect_fake(request: Request):
    try:
        normalized_text = preprocess_bangla_fake_news(request.text)
        result = fake_classifier(normalized_text)
        logger.info("Authentic: " + str(result))
        return JSONResponse(content={"Authentic:": result[0]['label'].split('_')[-1]})
    except Exception as e:
        logger.error('Error :'+ str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/detect_sentiment')
def detect_sentiment(request: Request):
    try:
        normalized_text = preprocess_bangla_text(request.text)
        result = sentiment_classifier(normalized_text)
        logger.info("Sentiment: " + str(result))
        return JSONResponse(content={"Sentiment": result[0]['label'].split('_')[-1]})
    except Exception as e:
        logger.error('Error :'+ str(e))
        raise HTTPException(status_code=500, detail=str(e))