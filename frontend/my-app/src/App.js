import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [inputText, setInputText] = useState('');
  const [analysisResults, setAnalysisResults] = useState([]);
  const [videoId, setVideoId] = useState('');
  const [channelUsername, setChannelUsername] = useState('');
  const [channelStats, setChannelStats] = useState(null);
  const [fakeAnalysis, setFakeAnalysis] = useState(false);
  const [maxResults, setMaxResults] = useState(50);
  const [youtubeComments, setYoutubeComments] = useState([]);

  const handleTextAnalysis = async () => {
    try {
      const response = await axios.post('http://localhost:8000/comment_analysis', {
        texts: inputText.split('\n').filter(text => text.trim() !== ''),
      }, { params: { fake_analysis: fakeAnalysis } });
      setAnalysisResults(response.data.results);
    } catch (error) {
      console.error('Error analyzing text:', error);
      alert('Failed to analyze text. Please check the console for details.');
    }
  };

  const handleVideoCommentAnalysis = async () => {
    try {
      const response = await axios.post('http://localhost:8000/youtube_comment_analysis', {
        video_id: videoId,
        max_results: parseInt(maxResults),
      }, { params: { fake_analysis: fakeAnalysis } });
      setAnalysisResults(response.data.results);
    } catch (error) {
      console.error('Error analyzing video comments:', error);
      alert('Failed to analyze video comments. Please check the console for details.');
    }
  };

  const handleChannelStats = async () => {
    try {
      const response = await axios.post('http://localhost:8000/get_channel_stats', {
        username: channelUsername,
      });
      setChannelStats(response.data);
    } catch (error) {
      console.error('Error fetching channel stats:', error);
      alert('Failed to fetch channel stats. Please check the console for details.');
    }
  };

  const handleFetchYoutubeComments = async () => {
    try {
      const response = await axios.post('http://localhost:8000/fetch_youtube_comments', {
        video_id: videoId,
        max_results: parseInt(maxResults),
      });
      setYoutubeComments(response.data.texts);
    } catch (error) {
      console.error('Error fetching Youtube comments:', error);
      alert('Failed to fetch Youtube comments. Please check the console for details.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Social Media Comment Analysis</h1>

      <div>
        <h2>Text Analysis</h2>
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter text to analyze (one per line)"
          rows={5}
          cols={50}
        />
        <br />
        <label>
          Fake Analysis:
          <input
            type="checkbox"
            checked={fakeAnalysis}
            onChange={(e) => setFakeAnalysis(e.target.checked)}
          />
        </label>
        <br />
        <button onClick={handleTextAnalysis}>Analyze Text</button>
      </div>

      <div>
        <h2>YouTube Video Comment Analysis</h2>
        <input
          type="text"
          value={videoId}
          onChange={(e) => setVideoId(e.target.value)}
          placeholder="Enter YouTube Video ID"
        />
        <input
          type="number"
          value={maxResults}
          onChange={(e) => setMaxResults(e.target.value)}
          placeholder="Max Results (default 50)"
        />
        <br />
        <label>
          Fake Analysis:
          <input
            type="checkbox"
            checked={fakeAnalysis}
            onChange={(e) => setFakeAnalysis(e.target.checked)}
          />
        </label>
        <br />
        <button onClick={handleVideoCommentAnalysis}>Analyze Video Comments</button>
        <button onClick={handleFetchYoutubeComments}>Fetch Youtube Comments</button>
        {youtubeComments.length > 0 && (
          <div>
            <h3>Fetched Comments:</h3>
            <ul>
              {youtubeComments.map((comment, index) => (
                <li key={index}>{comment}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <div>
        <h2>YouTube Channel Statistics</h2>
        <input
          type="text"
          value={channelUsername}
          onChange={(e) => setChannelUsername(e.target.value)}
          placeholder="Enter YouTube Channel Username"
        />
        <button onClick={handleChannelStats}>Get Channel Stats</button>
        {channelStats && (
          <div>
            <h3>Channel Statistics:</h3>
            <p>Channel ID: {channelStats.channel_id}</p>
            <p>Title: {channelStats.title}</p>
            <p>Description: {channelStats.description}</p>
            <p>Subscribers: {channelStats.subscriber_count}</p>
            <p>Videos: {channelStats.video_count}</p>
            <p>Views: {channelStats.view_count}</p>
          </div>
        )}
      </div>

      {analysisResults.length > 0 && (
        <div>
          <h2>Analysis Results</h2>
          <table style={{ borderCollapse: 'collapse', width: '100%' }}>
            <thead>
              <tr>
                <th style={{ border: '1px solid black', padding: '8px' }}>Original Text</th>
                <th style={{ border: '1px solid black', padding: '8px' }}>Converted Text</th>
                <th style={{ border: '1px solid black', padding: '8px' }}>Topic</th>
                <th style={{ border: '1px solid black', padding: '8px' }}>Emotion</th>
                <th style={{ border: '1px solid black', padding: '8px' }}>Spam</th>
                <th style={{ border: '1px solid black', padding: '8px' }}>Hate</th>
                <th style={{ border: '1px solid black', padding: '8px' }}>Sentiment</th>
                <th style={{ border: '1px solid black', padding: '8px' }}>Fake</th>
              </tr>
            </thead>
            <tbody>
              {analysisResults.map((result, index) => (
                <tr key={index}>
                  <td style={{ border: '1px solid black', padding: '8px' }}>{result.original_text}</td>
                  <td style={{ border: '1px solid black', padding: '8px' }}>{result.converted_text}</td>
                  <td style={{ border: '1px solid black', padding: '8px' }}>{result.topic}</td>
                  <td style={{ border: '1px solid black', padding: '8px' }}>{result.emotion}</td>
                  <td style={{ border: '1px solid black', padding: '8px' }}>{result.spam}</td>
                  <td style={{ border: '1px solid black', padding: '8px' }}>{result.hate}</td>
                  <td style={{ border: '1px solid black', padding: '8px' }}>{result.sentiment}</td>
                  <td style={{ border: '1px solid black', padding: '8px' }}>{result.fake}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;