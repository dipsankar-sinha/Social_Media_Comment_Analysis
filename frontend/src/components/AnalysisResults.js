import React from "react";

const AnalysisResultCard = ({ result, fakeAnalysis }) => {
  if (!result) return null; // Prevent render if result is undefined

  return (
    <div className="result-card">
      <div className="result-header">
        <p className="original-text">"{result.original_text}"</p>
        <p className="converted-text">({result.converted_text})</p>
      </div>
      <div className="result-details">
        <div className="result-item">
          <strong>Topic:</strong> {result.topic}
        </div>
        <div className="result-item">
          <strong>Emotion:</strong> {result.emotion}
        </div>
        <div className="result-item">
          <strong>Spam:</strong> {result.spam}
        </div>
        <div className="result-item">
          <strong>Hate:</strong> {result.hate}
        </div>
        <div className="result-item">
          <strong>Sentiment:</strong> {result.sentiment}
        </div>
        {fakeAnalysis && (
          <div className="result-item">
            <strong>Fake:</strong> {result.fake}
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisResultCard;
