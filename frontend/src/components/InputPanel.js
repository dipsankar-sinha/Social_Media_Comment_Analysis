import React from 'react';

function InputPanel({
  inputText, setInputText,
  videoID, setVideoID,
  maxResults, setMaxResults,
  channelUsername, setChannelUsername,
  channelID, setChannelID,
  fakeAnalysis, setFakeAnalysis,
  handleTextAnalysis,
  handleVideoCommentAnalysis,
  handleChannelStatsFetch
}) {
  return (
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
  );
}

export default InputPanel;