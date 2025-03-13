from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from backend.clean_text import preprocess_bangla_text, preprocess_bangla_fake_news
##from clean_text import preprocess_bangla_text, preprocess_bangla_fake_news
from backend.load import *

import json
import logging
import os

app = FastAPI()

 # Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Loading the classifiers for Hate Speech, Fake News and Sentiment Detection
fake_classifier = load_fake_classifier()
hate_classifier = load_hate_classifier()
sentiment_classifier = load_sentiment_classifier()

#Loading Gemini Model
gemini_model = load_gemini_model()

youtube = load_youtubev3_API()

# Request type
class TextRequest(BaseModel):
    texts: list[str]

class VideoRequest(BaseModel):
    video_id: str
    max_results: int = 50

class ChannelRequest(BaseModel): 
    username: Optional[str] = None
    channel_id: Optional[str] = None 
  

# Youtube Response 
class ChannelStatsResponse(BaseModel):
    channel_id: str
    title: str
    description: str
    subscriber_count: Optional[int] = None
    video_count: int
    view_count: int

class ChannelIDResponse(BaseModel):
    channel_id: str

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

# Function to fetch YouTube channel statistics
def fetch_channel_id(username: str) -> str:
    """Fetch channel ID using YouTube handle (@username)"""
    try:
        # Ensure handle starts with @
        if not username.startswith("@"):
            username = f"@{username.lstrip('@')}"

        request = youtube.channels().list(
            part="id",
            forHandle=username.strip()  # Correct parameter for handles
        )
        response = request.execute()

        if not response.get("items"):
            logger.error(f"No channel found for handle: {username}")
            raise HTTPException(status_code=404, detail="Channel not found")
            
        return response["items"][0]["id"]
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"ID Fetch Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Channel ID fetch failed")

def fetch_channel_stats(channel_id: str) -> ChannelStatsResponse:
    """Fetch complete channel statistics"""
    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()

        if not response.get("items"):
            logger.error(f"No data for channel ID: {channel_id}")
            raise HTTPException(status_code=404, detail="Channel data not found")

        data = response["items"][0]
        snippet = data["snippet"]
        stats = data.get("statistics", {})

        return ChannelStatsResponse(
            channel_id=channel_id,
            title=snippet["title"],
            description=snippet.get("description", ""),
            subscriber_count=int(stats["subscriberCount"]) if "subscriberCount" in stats else None,
            video_count=int(stats.get("videoCount", 0)),
            view_count=int(stats.get("viewCount", 0))
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Stats Fetch Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Statistics fetch failed")

# ===== API Endpoints =====
@app.post("/get_channel_id", response_model=ChannelIDResponse)
def get_channel_id(request: ChannelRequest):
    if not request.username:
        raise HTTPException(400, "Username required")
    return {"channel_id": fetch_channel_id(request.username)}

@app.post("/get_channel_stats", response_model=ChannelStatsResponse)
def get_channel_stats(request: ChannelRequest):
    if request.channel_id:
        return fetch_channel_stats(request.channel_id)
    if request.username:
        return fetch_channel_stats(fetch_channel_id(request.username))
    raise HTTPException(400, "Provide channel_id or username")

# Function to fetch YouTube comments
def fetch_youtube_comments(video_id: str, max_results: int = 50):
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results
        )
        response = request.execute()
        comments = [
            item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            for item in response.get("items", [])
        ]
        return comments
    except Exception as e:
        logger.error(f"Error fetching comments: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch YouTube comments.")

@app.get("/")
def index():
    logger.info("Index page accessed")
    return HTMLResponse(content="<h1>Welcome to Social Media Comment Analysis App using FASTAPI!</h1>")

@app.post("/fetch_youtube_comments")
def get_youtube_comments(request: VideoRequest) -> TextRequest:
    comments = fetch_youtube_comments(request.video_id, request.max_results)
    return TextRequest(texts=comments)

@app.post("/youtube_comment_analysis", response_model=TextResponse)
def youtube_comment_analysis(request: VideoRequest, fake_analysis: bool = False) -> TextResponse:
    try:
        # Fetch YouTube comments
        comments = fetch_youtube_comments(request.video_id, request.max_results)
        text_request = TextRequest(texts=comments)

        # Process comments
        results = process_text_with_gemini(text_request)
        results = process_hate(results)
        results = process_sentiment(results)
        if fake_analysis:
            results = process_fake_news(results)
        return results
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    
def process_text_with_gemini(request: TextRequest) -> TextResponse:
    prompt = f"""
            You are an advanced AI assistant specializing in **multilingual text analysis**, ensuring complete and accurate processing of text inputs in **Bengali (Indian & Bangladeshi), English, or Romanized Bengali**.

            ### **Instructions (STRICTLY FOLLOW THESE RULES)**
            1. **Text Conversion (Mandatory for ALL Inputs)**
               - If the input is in **English**, **translate** it into **pure Bengali**, including **cuss words, slang, and informal expressions**.
               - If the input is in **Romanized Bengali**, **transliterate** it into **pure Bengali**, maintaining accuracy.
               - If the input is already in **Bengali**, keep it unchanged.
               - **DO NOT OMIT, MODIFY, OR SOFTEN any words.**  
               - **English words MUST be converted—if no proper Bengali translation exists, transliterate them instead of leaving them unchanged.**  
               - **Ensure that the output is correct for both Indian Bengali and Bangladeshi Bengali speakers.**  

            2. **Classification Tasks (After Bengali Conversion)**
               - **Topic Classification**: Politics, Sports, Entertainment, Technology, Business, Health, Education, Other.
               - **Emotion Detection**: Happy, Sad, Angry, Fearful, Surprised, Neutral.
               - **Spam Detection**: Spam or Not Spam.

            3. **STRICT JSON Output Format**
               - **Return only JSON. No extra text, explanations, or comments.**
               - **Ensure the JSON is fully valid and parseable.**
               - **Every input must appear in `original_text` and its converted form in `converted_text`.**
               - **All `converted_text` must be fully in Bengali (translated or transliterated).**
               - **Cuss words, slang, and English terms must be accurately converted to Bengali (either translated or transliterated).**

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

            4. **Rules to Enforce Proper Execution**
               - **DO NOT OMIT ANY INPUTS**—Every text in the list must be processed.
               - **STRICTLY return only JSON, with no explanations, notes, or extra characters.**
               - **Ensure proper JSON formatting so it can be parsed without errors.**
               - **English words that lack proper Bengali translations MUST be transliterated into Bengali instead of being left unchanged.**
               - **Cuss words, slang, and offensive language must be accurately converted without filtering or modification.**
               - **Maintain appropriate word choices for both Indian Bengali and Bangladeshi Bengali audiences.**
               - **If a term has two Bengali variations, provide the one most commonly used across both regions.**
               - **Preserve the meaning and tone of the original text without distortion.**

            **Here are the texts to analyze:**
            {json.dumps(request.texts, ensure_ascii=False)}
            """
    response = gemini_model.generate_content(prompt)
    try:
        # Extract JSON content by stripping any unintended characters
        json_start = response.text.find("{")
        json_end = response.text.rfind("}") + 1
        cleaned_json = response.text[json_start:json_end]
        results = json.loads(cleaned_json)  # Convert to dictionary
        return TextResponse(
            results=results["results"]
        )
    except json.JSONDecodeError:
        raise Exception("Invalid response format")


def process_hate(request: TextRequest | TextResponse) -> TextResponse:
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

    return TextResponse(
        results=results
    )


def process_sentiment(request: TextRequest | TextResponse) -> TextResponse:
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
    return TextResponse(
        results=results
    )


def process_fake_news(request: TextRequest | TextResponse) -> TextResponse:
    results = []
    if isinstance(request, TextRequest):
        for text in request.texts:
            normalized_text = preprocess_bangla_fake_news(text)
            result = fake_classifier(normalized_text)
            logger.info(f"{text} -> [Authentic: {str(result)}]")
            results.append(
                TextAnalysisFormat(
                    converted_text=text,
                    fake='Fake' if int(result[0]['label'].split('_')[-1]) == 0 else 'Not Fake'
                )
            )
    else:
        for entry in request.results:
            text = entry.converted_text
            normalized_text = preprocess_bangla_fake_news(text)
            result = fake_classifier(normalized_text)
            logger.info(f"{text} -> [Authentic: {str(result)}]")
            entry.fake = 'Fake' if int(result[0]['label'].split('_')[-1]) == 0 else 'Not Fake'
            results.append(entry)
    return TextResponse(
        results=results
    )


@app.get('/')
def index():
    logger.info("Index page")
    logger.info(os.getcwd())
    return HTMLResponse(content="<h1>Welcome to Social Media Comment Analysis App using FASTAPI!</h1>")


#Calling Gemini API to handle English and Code_Switched or Romanized Bengali

@app.post('/analyze_texts_with_gemini', response_model=TextResponse)
def analyze_texts_with_gemini(request: TextRequest) -> TextResponse:
    try:
        return process_text_with_gemini(request)
    except Exception as e:
        logger.error('Error :' + str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/detect_hate', response_model=TextResponse)
def detect_hate(request: TextRequest | TextResponse) -> TextResponse:
    try:
        return process_hate(request)
    except Exception as e:
        logger.error('Error :' + str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/detect_fake_news')
def detect_fake_news(request: TextRequest | TextResponse) -> TextResponse:
    try:
        return process_fake_news(request)
    except Exception as e:
        logger.error('Error :' + str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/detect_sentiment')
def detect_sentiment(request: TextRequest | TextResponse) -> TextResponse:
    try:
        return process_sentiment(request)
    except Exception as e:
        logger.error('Error :' + str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/comment_analysis', response_model=TextResponse)
def comment_analysis(request: TextRequest, fake_analysis: bool = False) -> TextResponse:
    try:
        results = process_text_with_gemini(request)
        results = process_hate(results)
        results = process_sentiment(results)
        if fake_analysis:
            results = process_fake_news(results)
        return results
    except Exception as e:
        logger.error('Error :' + str(e))
        raise HTTPException(status_code=500, detail=str(e))
