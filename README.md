# Social Media Comment Analysis System

## 🧠 Overview

The Social Media Comment Analysis System is built using **FastAPI** and **Python** to analyze comments from platforms like YouTube. It leverages state-of-the-art NLP models to identify:

- **Sentiment**
- **Hate Speech**
- **Fake News**
- **Multilingual Inputs** (English, Bengali, Romanized Bengali, Code-switched)
- **Text Normalization**

The app processes text inputs and returns structured analysis results via RESTful API endpoints.

---

## 🚀 Used Technologies

### 💻 Language and Frameworks

- Python 3.10+
- FastAPI / Flask
- Pandas
- NumPy
- Scikit-learn
- Transformers (HuggingFace)
- PyTorch

### 🌐 Frontend

- React (via `npx create-react-app`)
- Axios (for HTTP requests)
- Recharts (for visualization)
- CORS Middleware (`fastapi.middleware.cors.CORSMiddleware`)

---

## 📦 Installation

### 🔧 Backend Setup

Install the required Python libraries:

```bash
pip install "fastapi[standard]"
pip install uvicorn
pip install transformers
pip install torch
```

### ▶️ Running the FastAPI App

Make sure you're in the root directory of the project. Run either of the following:

```bash
uvicorn backend.app:app --reload
# OR for Windows:
python.exe -m uvicorn backend.app:app --reload
```

---

## 🌐 Frontend Setup (React)

```bash
npx create-react-app my-app
cd my-app
npm install axios recharts
```

---

## ⚙️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Load React frontend |
| `POST` | `/get_channel_id` | Get YouTube channel ID from handle |
| `POST` | `/get_channel_stats` | Fetch YouTube channel stats |
| `POST` | `/fetch_youtube_comments` | Extract YouTube comments from video |
| `POST` | `/youtube_comment_analysis` | Analyze comments for sentiment, hate, fake news |
| `POST` | `/analyze_texts_with_gemini` | Use advanced model for text processing |
| `POST` | `/detect_hate` | Detect hate speech |
| `POST` | `/detect_fake_news` | Detect fake news |
| `POST` | `/detect_sentiment` | Run sentiment analysis |
| `POST` | `/comment_analysis` | Run full pipeline of all analyses |
| `GET` | `/trending_videos` | Get trending video data with metadata |

---

## 🔄 Processing Workflow

1. **Input Reception:** Receive text from user or YouTube.
2. **Preprocessing:** Normalize and clean text.
3. **Model Analysis:** NLP models analyze sentiment, hate, misinformation.
4. **Aggregation:** Results compiled into a structured JSON response.
5. **Output:** Return analysis to the requester.

---

## 🧑‍💻 Technical Overview

- **FastAPI**: High-performance backend framework
- **Pydantic**: For request validation and serialization
- **YouTube V3 API**: For video and channel metadata
- **CORS Middleware**: For secure cross-origin frontend-backend communication
- **HuggingFace Transformers**: For NLP classification tasks

---

## 📈 Key Features

- ✅ Sentiment Analysis
- ✅ Hate Speech Detection
- ✅ Fake News Detection
- ✅ Multilingual Input Support
- ✅ Text Conversion & Normalization
- ✅ YouTube Comment Fetching
- ✅ Channel Stats & Trending Info

---

## 📬 Contact

For any support or queries, feel free to open an issue or submit a pull request to contribute.
