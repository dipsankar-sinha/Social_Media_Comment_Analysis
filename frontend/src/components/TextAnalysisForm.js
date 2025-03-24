// src/components/TextAnalysisForm.js
import React from 'react';

const TextAnalysisForm = ({ inputText, setInputText, fakeAnalysis, setFakeAnalysis, handleTextAnalysis }) => (
  <div className="panel">
    <h2>Analyze Text</h2>
    <textarea
      value={inputText}
      onChange={(e) => setInputText(e.target.value)}
      placeholder="Enter text here..."
      rows={5}
      className="textarea"
    />
    <label>
      <input
        type="checkbox"
        checked={fakeAnalysis}
        onChange={() => setFakeAnalysis(!fakeAnalysis)}
      />
      Enable Fake News Detection
    </label>
    <button onClick={handleTextAnalysis} className="btn">Analyze Text</button>
  </div>
);

export default TextAnalysisForm;
