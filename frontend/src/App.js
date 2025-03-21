// src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [inputText, setInputText] = useState('');
  const [videoID, setVideoID] = useState('');
  const [channelUsername, setChannelUsername] = useState('');
  const [channelID, setChannelID] = useState('');
  const [maxResults, setMaxResults] = useState(50);
  const [analysisResults, setAnalysisResults] = useState([]);
  const [channelStats, setChannelStats] = useState(null);
  const [fakeAnalysis, setFakeAnalysis] = useState(false);
  const [subscriberChartData, setSubscriberChartData] = useState(null);
  const [showHomePage, setShowHomePage] = useState(true);
  const [showTopLists, setShowTopLists] = useState(false);
  const [trendingVideos, setTrendingVideos] = useState([]);


  useEffect(() => {
    const fetchTrendingVideos = async () => {
      try {
        const response = await axios.get('http://localhost:8000/trending_videos');
        setTrendingVideos(response.data.items);
      } catch (error) {
        console.error('Error fetching trending videos:', error);
        alert('Failed to fetch trending videos. Check console.');
      }
    };
    if (showHomePage) {
      fetchTrendingVideos();
    }
  }, [showHomePage]);

  const handleTextAnalysis = async () => {
    try {
      const response = await axios.post('http://localhost:8000/comment_analysis', {
        texts: inputText.split('\n').filter(text => text.trim() !== ''),
      }, {
        params: {
          fake_analysis: fakeAnalysis,
        },
      });
      setAnalysisResults(response.data.results);
      setShowHomePage(false);
      setShowTopLists(false);
    } catch (error) {
      console.error('Error analyzing text:', error);
      alert('Failed to analyze text. Check console for details.');
    }
  };

  const handleVideoCommentAnalysis = async () => {
    try {
      const response = await axios.post('http://localhost:8000/youtube_comment_analysis', {
        video_id: videoID,
        max_results: parseInt(maxResults),
      }, {
        params: {
          fake_analysis: fakeAnalysis,
        },
      });
      setAnalysisResults(response.data.results);
      setShowHomePage(false);
      setShowTopLists(false);
    } catch (error) {
      console.error('Error analyzing video comments:', error);
      alert('Failed to analyze video comments. Check console for details.');
    }
  };

  const handleChannelStatsFetch = async () => {
    try {
      let response;
      if (channelID) {
        response = await axios.post('http://localhost:8000/get_channel_stats', {
          channel_id: channelID,
        });
      } else if (channelUsername) {
        response = await axios.post('http://localhost:8000/get_channel_stats', {
          username: channelUsername,
        });
      } else {
        alert('Please provide either Channel ID or Username.');
        return;
      }
      setChannelStats(response.data);
      const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Aug','Sep','Oct','Nov','Dec'];
      const data = labels.map(() => Math.floor(Math.random() * 10000) + (response.data.subscriber_count || 0));
      setSubscriberChartData({
        labels: labels,
        datasets: [{
          label: 'Subscriber Growth',
          data: data,
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
        }],
      });
      setShowHomePage(false);
      setShowTopLists(false);
    } catch (error) {
      console.error('Error fetching channel stats:', error);
      alert('Failed to fetch channel stats. Check console for details.');
    }
  };

  const resetState = () => {
    setInputText('');
    setVideoID('');
    setChannelUsername('');
    setChannelID('');
    setMaxResults(50);
    setAnalysisResults([]);
    setChannelStats(null);
    setFakeAnalysis(false);
    setSubscriberChartData(null);
    setShowHomePage(true);
    setShowTopLists(false);
    setTrendingVideos([]);
  };

  const handleTopListsClick = () => {
    setShowHomePage(false);
    setShowTopLists(true);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo">Your Logo</div>
        <div className="search-bar">
          <input type="text" placeholder="Search..." />
          <button>Search</button>
        </div>
        <nav>
          <button onClick={resetState}>Home</button>
          <button onClick={handleTopListsClick}>Top Lists</button>
          <a href="/resources">Resources</a>
          <a href="/login">Login</a>
        </nav>
      </header>

      <main className="main-content">
        {showHomePage ? (
          <div className="left-panel">
            <div className="input-section">
              <h2>Text Analysis</h2>
              <textarea
                placeholder="Enter text to analyze (one per line)"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              />
              <label>
                <input
                  type="checkbox"
                  checked={fakeAnalysis}
                  onChange={(e) => setFakeAnalysis(e.target.checked)}
                />
                Include Fake News Analysis
              </label>
              <button onClick={handleTextAnalysis}>Analyze Text</button>
            </div>

            <div className="input-section">
              <h2>YouTube Video Comment Analysis</h2>
              <input
                type="text"
                placeholder="YouTube Video ID"
                value={videoID}
                onChange={(e) => setVideoID(e.target.value)}
              />
              <input
                type="number"
                placeholder="Max Results (default 50)"
                value={maxResults}
                onChange={(e) => setMaxResults(e.target.value)}
              />
              <label>
                <input
                  type="checkbox"
                  checked={fakeAnalysis}
                  onChange={(e) => setFakeAnalysis(e.target.checked)}
                />
                Include Fake News Analysis
              </label>
              <button onClick={handleVideoCommentAnalysis}>Analyze Video Comments</button>
            </div>

            <div className="input-section">
              <h2>YouTube Channel Statistics</h2>
              <input
                type="text"
                placeholder="Channel Username (@username)"
                value={channelUsername}
                onChange={(e) => setChannelUsername(e.target.value)}
              />
              <input
                type="text"
                placeholder="Channel ID"
                value={channelID}
                onChange={(e) => setChannelID(e.target.value)}
              />
              <button onClick={handleChannelStatsFetch}>Fetch Channel Stats</button>
            </div>
          </div>
        ) : showTopLists ? (
          <div className="right-panel">
            <h2>Trending YouTube Videos</h2>
            {trendingVideos.map((video) => (
              <div key={video.id.videoId} className="trending-video-card">
                <img src={video.snippet.thumbnails.medium.url} alt={video.snippet.title} />
                <h3>{video.snippet.title}</h3>
                <p>{video.snippet.description}</p>
                <a href={`https://www.youtube.com/watch?v=${video.id.videoId}`} target="_blank" rel="noopener noreferrer">Watch on YouTube</a>
              </div>
            ))}
          </div>
        ) : (
          <div className="right-panel">
            {channelStats && (
              <div className="channel-stats-card">
                <h3>Channel Statistics</h3>
                <p><strong>Channel ID:</strong> {channelStats.channel_id}</p>
                <p><strong>Title:</strong> {channelStats.title}</p>
                <p><strong>Description:</strong> {channelStats.description}</p>
                <p><strong>Subscribers:</strong> {channelStats.subscriber_count}</p>
                <p><strong>Videos:</strong> {channelStats.video_count}</p>
                <p><strong>Views:</strong> {channelStats.view_count}</p>
                {subscriberChartData && (
                  <div className="subscriber-chart">
                    <Line data={subscriberChartData} />
                  </div>
                )}
              </div>
            )}

{showHomePage && (
  <div className="popular-creators">
    <h2>Popular YouTube Creators</h2>
    <div className="results-grid">
      <div>Test 1</div>
      <div>Test 2</div>
    </div>
  </div>
)}
      

            {analysisResults.length > 0 && (
              <div className="results-section">
                <h2>Analysis Results</h2>
                <div className="results-grid">
                  {analysisResults.map((result, index) => (
                    <div key={index} className="result-card">
                      <p><strong>Original:</strong> {result.original_text}</p>
                      <p><strong>Converted:</strong> {result.converted_text}</p>
                      <p><strong>Topic:</strong> {result.topic}</p>
                      <p><strong>Emotion:</strong> {result.emotion}</p>
                      <p><strong>Spam:</strong> {result.spam}</p>
                      <p><strong>Hate:</strong> {result.hate}</p>
                      <p><strong>Sentiment:</strong> {result.sentiment}</p>
                      <p><strong>Fake:</strong> {result.fake}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 Your Company</p>
        <div className="footer-links">
          <a href="/terms">Terms</a>
          <a href="/privacy">Privacy</a>
          <a href="/contact">Contact</a>
        </div>
      </footer>
    </div>
  );
}

export default App;