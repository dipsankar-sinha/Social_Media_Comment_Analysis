// src/components/VideoAnalysisForm.js
import React from 'react';

const VideoAnalysisForm = ({
  videoID, setVideoID, maxResults, setMaxResults, fakeAnalysis, setFakeAnalysis, handleVideoCommentAnalysis
}) => (
  <div className="panel">
    <h2>Analyze Video Comments</h2>
    <input
      value={videoID}
      onChange={(e) => setVideoID(e.target.value)}
      placeholder="YouTube Video ID"
      className="input"
    />
    <input
      type="number"
      value={maxResults}
      onChange={(e) => setMaxResults(Number(e.target.value))}
      min={1}
      max={100}
      className="input"
    />
    <label>
      <input
        type="checkbox"
        checked={fakeAnalysis}
        onChange={() => setFakeAnalysis(!fakeAnalysis)}
      />
      Enable Fake News Detection
    </label>
    <button onClick={handleVideoCommentAnalysis} className="btn">Analyze Comments</button>
  </div>
);

export default VideoAnalysisForm;
