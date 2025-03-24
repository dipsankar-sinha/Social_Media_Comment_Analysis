// src/components/ChannelStatsForm.js
import React from 'react';

const ChannelStatsForm = ({ channelUsername, setChannelUsername, channelID, setChannelID, handleChannelStatsFetch }) => (
  <div className="panel">
    <h2>Get Channel Stats</h2>
    <input
      value={channelUsername}
      onChange={(e) => setChannelUsername(e.target.value)}
      placeholder="YouTube Username"
      className="input"
    />
    <input
      value={channelID}
      onChange={(e) => setChannelID(e.target.value)}
      placeholder="YouTube Channel ID"
      className="input"
    />
    <button onClick={handleChannelStatsFetch} className="btn">Fetch Stats</button>
  </div>
);

export default ChannelStatsForm;
