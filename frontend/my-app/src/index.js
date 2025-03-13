import React from 'react';
import ReactDOM from 'react-dom/client'; // Import createRoot
import App from './App'; // Assuming your main component is in App.js

const root = ReactDOM.createRoot(document.getElementById('root')); // Create a root
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);