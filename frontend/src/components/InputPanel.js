import React from "react";

function InputPanel({
  inputText,
  setInputText,
  videoID,
  setVideoID,
  maxResults,
  setMaxResults,
  channelUsername,
  setChannelUsername,
  channelID,
  setChannelID,
  channelInputType,
  setChannelInputType,
  fakeAnalysis,
  setFakeAnalysis,
  handleTextAnalysis,
  handleVideoCommentAnalysis,
  handleChannelStatsFetch,
}) {
  return (
    <div className="input-panel">
      <div className="input-section">
        <h2>Text Analysis</h2>
        <textarea
          placeholder="Enter texts to analyze (one per line)"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <label>
          Include Fake News Analysis
          <input
            type="checkbox"
            checked={fakeAnalysis}
            onChange={(e) => setFakeAnalysis(e.target.checked)}
          />
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
          placeholder="Max Results (default 10)"
          value={maxResults}
          onChange={(e) => setMaxResults(e.target.value)}
        />
        <button onClick={() => handleVideoCommentAnalysis(videoID)}>
          Analyze Video Comments
        </button>
      </div>

      <div className="input-section">
        <h2>YouTube Channel Statistics</h2>
        <div className="radio-options">
          <label>
            <input
              type="radio"
              name="channelInput"
              value="username"
              checked={channelInputType === "username"}
              onChange={() => {
                setChannelInputType("username");
                setChannelID("");
              }}
            />
            Username
          </label>
          <label>
            <input
              type="radio"
              name="channelInput"
              value="channelID"
              checked={channelInputType === "channelID"}
              onChange={() => {
                setChannelInputType("channelID");
                setChannelUsername("");
              }}
            />
            Channel ID
          </label>
        </div>
        {channelInputType === "username" ? (
          <input
            type="text"
            placeholder="Channel Username (@username)"
            value={channelUsername}
            onChange={(e) => setChannelUsername(e.target.value)}
          />
        ) : (
          <input
            type="text"
            placeholder="Channel ID"
            value={channelID}
            onChange={(e) => setChannelID(e.target.value)}
          />
        )}
        <button onClick={handleChannelStatsFetch}>Fetch Channel Stats</button>
      </div>
    </div>
  );
}

export default InputPanel;
