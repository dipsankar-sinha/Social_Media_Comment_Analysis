// src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DOMPurify from 'dompurify';

import './App.css';
import './Futuristic.css';
import Loader from './Loader';
import Header from './components/Header';
import InputPanel from './components/InputPanel';
import TrendingVideos from './components/TrendingVideos';
import ChannelStatsCard from './components/ChannelStatsCard';
import AnalysisResults from './components/AnalysisResults';
import Footer from './components/Footer';

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
  const [loading, setLoading] = useState(false);
  const [htmlContent, setHtmlContent] = useState(""); // State to store HTML content

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
      setLoading(true);
      const response = await axios.post('http://localhost:8000/comment_analysis', {
        texts: inputText.split('\n').filter(text => text.trim() !== ''),
      }, {
        params: { fake_analysis: fakeAnalysis },
      });
      setAnalysisResults(response.data.results);
      setShowHomePage(false);
      setShowTopLists(false);
    } catch (error) {
      console.error('Error analyzing text:', error);
      alert('Failed to analyze text. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  const handleVideoCommentAnalysis = async () => {
    try {
      setLoading(true);
      const response = await axios.post('http://localhost:8000/youtube_comment_analysis', {
        video_id: videoID,
        max_results: parseInt(maxResults),
      }, {
        params: { fake_analysis: fakeAnalysis },
      });
      setAnalysisResults(response.data.results);
      setShowHomePage(false);
      setShowTopLists(false);
    } catch (error) {
      console.error('Error analyzing video comments:', error);
      alert('Failed to analyze video comments. Check console for details.');
    } finally {
      setLoading(false);
    }
  };
  const handleAboutUs = async (event)=> {
    try {
      event.preventDefault(); // Prevent default anchor behavior (navigation)
      setLoading(true);
      if (htmlContent === ''){
        let response= await axios.get('http://localhost:8000/');
        const rawHtml = response.data;
        // Sanitize the fetched HTML
        const sanitizedHtml = DOMPurify.sanitize(rawHtml);
        setHtmlContent(sanitizedHtml); // Update state with the fetched HTML
      } else {
        setHtmlContent('');
      }
    } catch(error) {
      console.error('Error while accessing the information:', error);
      alert('Failed to access the page. Check console for details.');
      setHtmlContent("<p>Failed to load content. Please try again.</p>");
    } finally {
      setLoading(false);
    }
  };

  const handleChannelStatsFetch = async () => {
    try {
      setLoading(true);
      let response;
      if (channelID) {
        response = await axios.post('http://localhost:8000/get_channel_stats', { channel_id: channelID });
      } else if (channelUsername) {
        response = await axios.post('http://localhost:8000/get_channel_stats', { username: channelUsername });
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
    } finally {
      setLoading(false);
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
    setHtmlContent('');
  };

  const handleTopListsClick = () => {
    setShowHomePage(false);
    setShowTopLists(true);
  };

  return (
    <div className="app-container futuristic">
      {loading && <Loader />}
      <Header resetState={resetState} handleTopListsClick={handleTopListsClick} />
      <main className="main-content">
        {showHomePage ? (
          <InputPanel
            inputText={inputText}
            setInputText={setInputText}
            videoID={videoID}
            setVideoID={setVideoID}
            channelUsername={channelUsername}
            setChannelUsername={setChannelUsername}
            channelID={channelID}
            setChannelID={setChannelID}
            maxResults={maxResults}
            setMaxResults={setMaxResults}
            fakeAnalysis={fakeAnalysis}
            setFakeAnalysis={setFakeAnalysis}
            handleTextAnalysis={handleTextAnalysis}
            handleVideoCommentAnalysis={handleVideoCommentAnalysis}
            handleChannelStatsFetch={handleChannelStatsFetch}
          />
        ) : showTopLists ? (
          <TrendingVideos trendingVideos={trendingVideos} />
        ) : (
          <div className="right-panel">
            {channelStats && <ChannelStatsCard channelStats={channelStats} subscriberChartData={subscriberChartData} />}
            {analysisResults.length > 0 && (
              <div className="results-section">
                <h2>Analysis Results</h2>
                <div className="results-grid">
                  {analysisResults.map((result, index) => (
                    <AnalysisResults key={index} result={result} />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </main>
      <Footer handleAboutUs={handleAboutUs} htmlContent={htmlContent}/>
    </div>
  );
}

export default App;
