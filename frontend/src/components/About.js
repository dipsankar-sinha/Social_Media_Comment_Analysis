import React from "react";

function About() {
  return (
    <div className="result-panel">
      <div className="about">
        <header>
          <h2>About</h2>
        </header>
        <div className="container">
          <section id="overview">
            <h3>Overview</h3>
            <p>
              The Social Media Comment Analysis App is built using FastAPI and
              Python to analyze comments from social media platforms. It
              leverages advanced natural language processing techniques to
              provide analysis on sentiment, hate speech, fake news, and more.
            </p>
            <p>
              The system processes input text from various sources, particularly
              YouTube, and returns structured results via multiple API
              endpoints.
            </p>
          </section>

          <section id="features">
            <h3>Key Features</h3>
            <div className="features">
              <div className="feature">
                <h4>Sentiment Analysis</h4>
                <p>
                  Determine if a comment expresses positive or negative
                  sentiment.
                </p>
              </div>
              <div className="feature">
                <h4>Hate Speech Detection</h4>
                <p>
                  Identify offensive or harmful language to maintain a
                  respectful environment.
                </p>
              </div>
              <div className="feature">
                <h4>Fake News Detection</h4>
                <p>
                  Assess content to flag potentially misleading or false
                  information.
                </p>
              </div>
              <div className="feature">
                <h4>Multilingual Support</h4>
                <p>
                  Handle English, Bengali, Romanized Bengali, and code-switched
                  text.
                </p>
              </div>
              <div className="feature">
                <h4>Text Conversion & Normalization</h4>
                <p>
                  Convert and normalize text inputs for consistent processing.
                </p>
              </div>
            </div>
          </section>

          <section id="api-endpoints">
            <h3>API Endpoints</h3>
            <p>
              The application exposes a set of RESTful endpoints. Some of the
              main ones include:
            </p>
            <ul>
              <li>
                <strong>GET /</strong>: React Web Application
              </li>
              <li>
                <strong>POST /get_channel_id</strong>: Retrieve a channel
                identifier based on a provided handle.
              </li>
              <li>
                <strong>POST /get_channel_stats</strong>: Fetch public
                statistics for a given channel.
              </li>
              <li>
                <strong>POST /fetch_youtube_comments</strong>: Extract comments
                from a specified YouTube video.
              </li>
              <li>
                <strong>POST /youtube_comment_analysis</strong>: Analyze
                comments for sentiment, hate speech, and fake news.
              </li>
              <li>
                <strong>POST /analyze_texts_with_gemini</strong>: Process text
                using an advanced conversion model.
              </li>
              <li>
                <strong>POST /detect_hate</strong>: Execute hate speech
                detection.
              </li>
              <li>
                <strong>POST /detect_fake_news</strong>: Perform fake news
                detection.
              </li>
              <li>
                <strong>POST /detect_sentiment</strong>: Run sentiment analysis
                on provided texts.
              </li>
              <li>
                <strong>POST /comment_analysis</strong>: A comprehensive
                endpoint that aggregates various analyses.
              </li>
              <li>
                <strong>GET /trending_videos</strong>: Retrieve trending videos
                with essential metadata.
              </li>
            </ul>
          </section>

          <section id="workflow">
            <h3>Processing Workflow</h3>
            <ol>
              <li>
                <strong>Input Reception:</strong> The system receives text
                inputs from various sources (e.g., YouTube comments).
              </li>
              <li>
                <strong>Preprocessing:</strong> Input text is normalized and
                converted as needed.
              </li>
              <li>
                <strong>Model Analysis:</strong> Advanced models analyze the
                text for sentiment, hate speech, and misinformation.
              </li>
              <li>
                <strong>Aggregation:</strong> The results are compiled into a
                structured JSON response.
              </li>
              <li>
                <strong>Output:</strong> The API returns the analysis to the
                requester.
              </li>
            </ol>
          </section>

          <section id="technical">
            <h3>Technical Overview</h3>
            <p>
              The backend is built on FastAPI, ensuring a fast and scalable REST
              API. The system uses:
            </p>
            <ul>
              <li>Python for server-side logic and data processing.</li>
              <li>Pydantic for data validation and serialization.</li>
              <li>CORS middleware to enable secure cross-origin requests.</li>
              <li>
                Integration with the YouTube V3 API to fetch video and channel
                data.
              </li>
              <li>
                Advanced NLP models for text conversion and classification
                without exposing internal implementation details.
              </li>
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
}

export default About;
