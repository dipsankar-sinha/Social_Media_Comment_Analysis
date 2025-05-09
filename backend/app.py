from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.clean_text import *
from backend.load import *

import json
import logging

app = FastAPI()


#Here Frontend and Backend will be on same device and same port
#SO, No need of CORS Middleware

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Loading the classifiers for Hate Speech, Fake News and Sentiment Detection
fake_classifier = load_fake_classifier()
hate_classifier = load_hate_classifier()
sentiment_classifier = load_sentiment_classifier()

# Loading Gemini Model
gemini_model = load_gemini_model("gemini-2.0-flash")

# Loading YouTube V3 API
youtube = load_youtube_v3()

# Text Request type ---> Gemini and Other Trained Models
class TextRequest(BaseModel):
    texts: list[str]

# Video Request type ---> YouTube V3 API
class VideoRequest(BaseModel):
    video_id: str
    max_results: int = 10

# Channel Request type ---> YouTube V3 API
class ChannelRequest(BaseModel): 
    username: str | None = None
    channel_id: str | None = None
    video_id: str | None = None
  

# Different YouTube Response and format types <--- YouTube V3 API
class ChannelStatsResponse(BaseModel):
    channel_id: str
    title: str
    description: str
    subscriber_count: int | None = None
    video_count: int
    view_count: int
    videos: list[dict] | None = None

class ChannelIDResponse(BaseModel):
    channel_id: str

class TrendingVideo(BaseModel):
    id: dict
    snippet: dict

class TrendingVideosResponse(BaseModel):
    items: list[TrendingVideo]

# Response format for each text
class TextAnalysisFormat(BaseModel):
    original_text: str | None = None
    converted_text: str
    topic: str | None = None
    emotion: str | None = None
    spam: str | None = None
    hate: str | None = None
    sentiment: str | None = None
    fake: str | None = None

# Response type <--- Gemini and Other Trained Models
class TextResponse(BaseModel):
    results: list[TextAnalysisFormat]

class EmotionPercentage(BaseModel):
    Happy: float
    Sad: float
    Angry: float
    Fearful: float
    Surprised: float
    Neutral: float

class TopicPercentage(BaseModel):
    Politics: float
    Sports: float
    Entertainment: float
    Technology: float
    Business: float
    Health: float
    Education: float
    Other: float

class AnalysisResults(BaseModel):
    hate_speech: dict[str, float]  # e.g., {"percentage": value}
    sentiment: dict[str, float]  # e.g., {"positive_percentage": value}
    fake_news: dict[str, float]  # e.g., {"percentage": value}
    spam: dict[str, float]  # e.g., {"percentage": value}
    emotion: dict[str, EmotionPercentage]  # e.g., {"percentage": EmotionPercentage(...) }
    topic: dict[str, TopicPercentage]  # e.g., {"percentage": TopicPercentage(...) }

#Response type <--- Final Analysis Report
class FinalAnalysisResponse(BaseModel):
    results: list[TextAnalysisFormat]
    aggregate_stats: AnalysisResults | None

# Function to fetch YouTube channel statistics
def fetch_channel_id(username: str = None, video_id: str = None) -> str:
    """Fetch channel ID using YouTube handle (@username)"""
    try:
        if username:
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

        elif video_id:
            # Fetch video details
            request = youtube.videos().list(
                part="snippet",
                id=video_id
            )
            response = request.execute()
            if not response.get("items"):
                logger.error(f"No channel found for handle: {username}")
                raise HTTPException(status_code=404, detail="Channel not found")
            return response["items"][0]["snippet"]["channelId"]

        else:
            logger.error("Invalid input, Try again!")
            raise HTTPException(status_code=404, detail="Invalid input, Try again!")

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

        # Fetch recent videos
        videos = fetch_channel_videos(channel_id)

        return ChannelStatsResponse (
            channel_id=channel_id,
            title=snippet["title"],
            description=snippet.get("description", ""),
            subscriber_count=int(stats["subscriberCount"]) if "subscriberCount" in stats else None,
            video_count=int(stats.get("videoCount", 0)),
            view_count=int(stats.get("viewCount", 0)),
            videos=videos, # Add videos to the response
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Stats Fetch Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Statistics fetch failed")
    
def fetch_channel_videos(channel_id: str, max_results: int = 5) -> list[dict]:
    """Fetch recent videos from a channel."""
    try:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="date",
            type="video",
            maxResults=max_results,
        )
        response = request.execute()
        videos = []
        for item in response.get("items", []):
            videos.append({
                "video_id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"],
            })
        return videos
    except Exception as e:
        logger.error(f"Video Fetch Error: {str(e)}")
        return []

def aggregate_results(results: TextResponse) -> AnalysisResults:
    """Aggregate classification results into percentages for all features."""
    total = len(results.results)
    emotions = ['Happy', 'Sad', 'Angry', 'Fearful', 'Surprised', 'Neutral']
    topics = ['Politics', 'Sports', 'Entertainment', 'Technology', 'Business', 'Health', 'Education', 'Other']

    if total == 0:
        return AnalysisResults(
            hate_speech={"percentage": 0},
            sentiment={"positive_percentage": 0},
            fake_news={"percentage": 0},
            spam={"percentage": 0},
            emotion={"percentage": EmotionPercentage(**{emotion: 0 for emotion in emotions})},
            topic={"percentage": TopicPercentage(**{topic: 0 for topic in topics})},
        )

    # Aggregate counts
    hate_count = sum(1 for r in results.results if r.hate == 'Hate')
    positive_sentiment_count = sum(1 for r in results.results if r.sentiment == 'Positive')
    fake_count = sum(1 for r in results.results if r.fake == 'Fake')
    spam_count = sum(1 for r in results.results if r.spam == 'Spam')

    # Aggregate counts for emotions and topics
    emotion_counts = {emotion: sum(1 for r in results.results if r.emotion == emotion) for emotion in emotions}
    topic_counts = {topic: sum(1 for r in results.results if r.topic == topic) for topic in topics}

    # Construct the result dictionary
    return AnalysisResults(
        hate_speech={"percentage": round(hate_count / total * 100, 2)},
        sentiment={"positive_percentage": round(positive_sentiment_count / total * 100, 2 )},
        fake_news={"percentage": round(fake_count / total * 100, 2 )},
        spam={"percentage": round(spam_count / total * 100, 2 )},
        emotion={"percentage": EmotionPercentage(**{emotion: round(count / total * 100, 2) for emotion, count in emotion_counts.items()})},
        topic={"percentage": TopicPercentage(**{topic: round(count / total * 100, 2) for topic, count in topic_counts.items()})},
    )
    
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

# ===== API Endpoints =====
@app.post("/get_channel_id", response_model=ChannelIDResponse)
def get_channel_id(request: ChannelRequest):
    if request.video_id:
        return {"channel_id": fetch_channel_id(video_id = request.video_id)}
    if request.username:
        return {"channel_id": fetch_channel_id(username=request.username)}
    raise HTTPException(400, "Either username or video-id required")


@app.post("/get_channel_stats", response_model=ChannelStatsResponse)
def get_channel_stats(request: ChannelRequest):
    if request.channel_id:
        return fetch_channel_stats(request.channel_id)
    if request.username:
        return fetch_channel_stats(fetch_channel_id(username=request.username))
    if request.video_id:
        return fetch_channel_stats(fetch_channel_id(video_id=request.video_id))
    raise HTTPException(400, "Provide channel_id or username")

# Function to fetch YouTube comments
def fetch_youtube_comments(video_id: str, max_results: int = 10):
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
        return clean_api_texts(comments) #Applying initial cleaning
    except Exception as e:
        logger.error(f"Error fetching comments: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch YouTube comments.")

@app.post("/fetch_youtube_comments")
def get_youtube_comments(request: VideoRequest) -> TextRequest:
    comments = fetch_youtube_comments(request.video_id, request.max_results)
    return TextRequest(texts=comments)


@app.post("/youtube_comment_analysis", response_model=FinalAnalysisResponse)
def youtube_comment_analysis(request: VideoRequest, fake_analysis: bool = False) -> FinalAnalysisResponse:
    try:
        logger.error(f"Video_id : {request.video_id}, Max Results: {request.max_results}")
        # Fetch YouTube comments
        comments = fetch_youtube_comments(request.video_id, request.max_results)
        text_request = TextRequest(texts=comments)

        # Process comments
        results = process_text_with_gemini(text_request)
        results = process_hate(results)
        results = process_sentiment(results)

        if fake_analysis:
            results = process_fake_news(results)

        # Ensure results are in the correct format
        if isinstance(results, TextResponse):
            # Add aggregated statistics
            aggregated_stats = aggregate_results(results)
            # Return the response
            return FinalAnalysisResponse(results=results.results, aggregate_stats=aggregated_stats)
        else:
            raise HTTPException(status_code=500, detail="Failed to fetch YouTube comments.")

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
    
@app.get("/trending_videos")
def get_trending_videos():
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode="IN",
            maxResults=10,  # Added maxResults
        )
        response = request.execute()
        # Example of returning only necessary data (optional)
        simplified_items = []
        for item in response.get('items', []):
            simplified_items.append({
                'id': item['id'],
                'snippet': {
                    'title': item['snippet']['title'],
                    'thumbnails': item['snippet']['thumbnails']
                }
            })
        return {'items': simplified_items} #return only the needed information.
    except Exception as e:
        logging.error(f"Error fetching trending videos: {e} - Response: {response if 'response' in locals() else 'No response'}") # added response to the log.
        raise HTTPException(status_code=500, detail="Failed to fetch trending videos.")


#Serve React build directory ---> Frontend EndPoint
app.mount("/", StaticFiles(directory="./frontend/build", html=True), name="frontend")


    