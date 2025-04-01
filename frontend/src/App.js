import React, { useState, useEffect } from "react";
import axios from "axios";

import "./App.css";
import Loader from "./Loader";
import Header from "./components/Header";
import InputPanel from "./components/InputPanel";
import TrendingVideos from "./components/TrendingVideos";
import ChannelStatsCard from "./components/ChannelStatsCard";
import AnalysisResults from "./components/AnalysisResults";
import AnalysisCharts from "./components/AnalysisCharts";
import Footer from "./components/Footer";
import Contact from "./components/Contact";
import About from "./components/About";

function App() {
  //axios.defaults.baseURL = "http://localhost:8000"; // Backend URL
  //Commenting This the frontend and backend in running on same port in same machine.
  axios.defaults.baseURL = "/";

  //Setting Global Variables
  const [showHomePage, setShowHomePage] = useState(true);
  const [showTopLists, setShowTopLists] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [showAnalysisResults, setShowAnalysisResults] = useState(false);
  const [showAnalysisCharts, setShowAnalysisCharts] = useState(true);
  const [showContactPage, setShowContactPage] = useState(false);
  const [showAbout, setShowAbout] = useState(false);

  const [loading, setLoading] = useState(false);
  const [inputText, setInputText] = useState("");
  const [videoID, setVideoID] = useState("");

  const [channelInputType, setChannelInputType] = useState("username");
  const [channelUsername, setChannelUsername] = useState("");
  const [channelID, setChannelID] = useState("");

  const [trendingVideos, setTrendingVideos] = useState([]);
  const [maxResults, setMaxResults] = useState(10);
  const [analysisResults, setAnalysisResults] = useState([]);
  const [analysisCharts, setAnalysisCharts] = useState(null);
  const [channelStats, setChannelStats] = useState(null);
  const [fakeAnalysis, setFakeAnalysis] = useState(false);

  const resetState = () => {
    setShowHomePage(true);
    setShowTopLists(false);
    setShowResults(false);
    setShowAnalysisResults(false);
    setShowAnalysisCharts(true);
    setShowContactPage(false);
    setShowAbout(false);

    setInputText("");
    setFakeAnalysis(false);
    setMaxResults(10);
    setChannelUsername("");
    setChannelID("");
    setChannelInputType("username");

    setVideoID("");
    setAnalysisResults([]);
    setChannelStats(null);
    setTrendingVideos([]);
    setAnalysisCharts(null);
  };

  useEffect(() => {
    const fetchTrendingVideos = async () => {
      try {
        const response = await axios.get("/trending_videos");
        setTrendingVideos(response.data.items);
      } catch (error) {
        console.error("Error fetching trending videos:", error);
        alert("Failed to fetch trending videos. Check console.");
      }
    };
    if (showHomePage || trendingVideos.length === 0) {
      fetchTrendingVideos();
    }
  }, [showHomePage, trendingVideos.length]);
  useEffect(
    () => window.scrollTo(0, 0),
    [showHomePage, showTopLists, showContactPage, showAbout],
  );
  const handleTextAnalysis = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        "/comment_analysis",
        {
          texts: inputText.split("\n").filter((text) => text.trim() !== ""),
        },
        {
          params: { fake_analysis: fakeAnalysis },
        },
      );
      setAnalysisResults(response.data.results);

      setChannelStats(null);
      setShowHomePage(false);
      setShowTopLists(false);
      setShowResults(true);
      setShowAnalysisResults(true);
      setShowAnalysisCharts(false);
    } catch (error) {
      console.error("Error analyzing text:", error);
      alert("Failed to analyze text. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const handleVideoCommentAnalysis = async (videoID) => {
    try {
      setLoading(true);
      const response = await axios.post(
        "/youtube_comment_analysis",
        {
          video_id: videoID,
          max_results: maxResults,
        },
        {
          params: { fake_analysis: fakeAnalysis },
        },
      );
      setAnalysisResults(response.data.results);
      setAnalysisCharts(response.data.aggregate_stats);

      setChannelStats(null);
      setShowHomePage(false);
      setShowTopLists(false);
      setShowAbout(false);
      setShowResults(true);
      setShowAnalysisResults(false);
      setShowAnalysisCharts(true);
    } catch (error) {
      console.error("Error analyzing video comments:", error);
      alert("Failed to analyze video comments. Check console for details.");
    } finally {
      setLoading(false);
    }
  };
  const toggleAnalysisCharts = () => {
    setShowAnalysisCharts((prev) => !prev);
  };
  const toggleAnalysisResults = () => {
    setShowAnalysisResults((prev) => !prev);
  };
  const handleChannelStatsFetch = async () => {
    try {
      setLoading(true);
      let response;

      if (channelInputType === "channelID" && channelID) {
        response = await axios.post("/get_channel_stats", {
          channel_id: channelID,
        });
      } else if (channelInputType === "username" && channelUsername) {
        response = await axios.post("/get_channel_stats", {
          username: channelUsername,
        });
      } else {
        alert("Please enter a valid input.");
        setLoading(false);
        return;
      }

      setChannelStats(response.data);

      setShowResults(true);
      setShowHomePage(false);
      setShowTopLists(false);
      setShowAbout(false);
      setShowContactPage(false);
    } catch (error) {
      console.error("Error fetching channel stats:", error);
      alert("Failed to fetch channel stats. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const handleChannelStatsFetchFromVideoID = async (videoID) => {
    try {
      setLoading(true);
      let response = await axios.post("/get_channel_id", {
        video_id: videoID,
      });
      const newChannelID = response.data.channel_id;
      if (!newChannelID) {
        alert("No channel ID found for this video.");
        return;
      }
      let statsResponse = await axios.post("/get_channel_stats", {
        channel_id: newChannelID,
      });

      setChannelID(newChannelID);
      setShowResults(true);
      setChannelStats(statsResponse.data);
      setShowHomePage(false);
      setShowTopLists(false);
      setShowAbout(false);
      setShowAbout(false);
    } catch (error) {
      console.error("Error fetching channel ID:", error);
      alert("Failed to fetch channel ID. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const handleTopListsClick = () => {
    setShowHomePage(false);
    setShowTopLists(true);
    setShowResults(false);
    setShowContactPage(false);
    setShowAbout(false);
  };

  const handleAbout = async (event) => {
    try {
      event.preventDefault();
      setShowHomePage(false);
      setShowTopLists(false);
      setShowContactPage(false);
      setShowResults(false);
      setLoading(false);
      setShowAbout(true);
    } catch (error) {
      console.error("Error while accessing the information:", error);
      alert("Failed to access the page. Check console for details.");
    }
  };
  const handleContact = async (event) => {
    try {
      event.preventDefault();
      setLoading(false);
      setShowHomePage(false);
      setShowTopLists(false);
      setShowResults(false);
      setShowAbout(false);
      setShowContactPage(true);
    } catch (error) {
      console.error("Error while accessing the contact page:", error);
      alert("Failed to access the page. Check console for details.");
    }
  };
  return (
    <div className="app-container">
      {loading && <Loader />}
      <Header
        resetState={resetState}
        handleTopListsClick={handleTopListsClick}
      />
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
            channelInputType={channelInputType}
            setChannelInputType={setChannelInputType}
            maxResults={maxResults}
            setMaxResults={setMaxResults}
            fakeAnalysis={fakeAnalysis}
            setFakeAnalysis={setFakeAnalysis}
            handleTextAnalysis={handleTextAnalysis}
            handleVideoCommentAnalysis={handleVideoCommentAnalysis}
            handleChannelStatsFetch={handleChannelStatsFetch}
          />
        ) : (
          (showTopLists && (
            <TrendingVideos
              trendingVideos={trendingVideos}
              maxResults={maxResults}
              setMaxResults={setMaxResults}
              setVideoID={setVideoID}
              handleVideoCommentAnalysis={handleVideoCommentAnalysis}
              handleChannelStatsFetchFromVideoID={
                handleChannelStatsFetchFromVideoID
              }
            />
          )) ||
          (showResults && (
            <div className="result-panel">
              {channelStats && (
                <ChannelStatsCard
                  channelStats={channelStats}
                  maxResults={maxResults}
                  setMaxResults={setMaxResults}
                  handleVideoCommentAnalysis={handleVideoCommentAnalysis}
                />
              )}
              {analysisResults.length > 0 && (
                <div className="results-section">
                  <button onClick={toggleAnalysisResults} className="dropdown">
                    {showAnalysisResults ? (
                      <h2>Analysis Results ▲</h2>
                    ) : (
                      <h2>Analysis Results ▼</h2>
                    )}
                  </button>
                  {showAnalysisResults && (
                    <div className="results-grid">
                      {analysisResults.map((result, index) => (
                        <AnalysisResults
                          key={index}
                          result={result}
                          fakeAnalysis={fakeAnalysis}
                        />
                      ))}
                    </div>
                  )}
                  {analysisCharts && (
                    <div className="charts-section">
                      <button
                        onClick={toggleAnalysisCharts}
                        className="dropdown"
                      >
                        {showAnalysisCharts ? (
                          <h2>Aggregate Statistics ▲</h2>
                        ) : (
                          <h2>Aggregate Statistics ▼</h2>
                        )}
                      </button>
                      {showAnalysisCharts && (
                        <div className="results-grid">
                          <AnalysisCharts analysisCharts={analysisCharts} />
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        )}
        {showContactPage && <Contact />}
        {showAbout && <About />}
      </main>
      <Footer handleAbout={handleAbout} handleContact={handleContact} />
    </div>
  );
}

export default App;
