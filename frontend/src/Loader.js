// src/components/Loader.js
import React from 'react';
import './Futuristic.css';

const Loader = () => {
  return (
    <div className="loader-backdrop">
      <div className="holo-loader">
        <div className="holo-glow"></div>
        <div className="holo-core">Loading...</div>
      </div>
    </div>
  );
};

export default Loader;
