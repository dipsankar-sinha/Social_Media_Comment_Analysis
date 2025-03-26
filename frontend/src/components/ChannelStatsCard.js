import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

const ChannelStatsCard = ({ channelStats, subscriberChartData }) => {
  const [showChart, setShowChart] = useState(false);

  const toggleChart = () => {
    setShowChart((prev) => !prev);
  };

  return (
    <div className="channel-stats-card">
      <h3>Channel Statistics</h3>
      <p><strong>Channel ID:</strong> {channelStats.channel_id}</p>
      <p><strong>Title:</strong> {channelStats.title}</p>
      <p><strong>Description:</strong> {channelStats.description}</p>
      <p><strong>Subscribers:</strong> {channelStats.subscriber_count || 'N/A'}</p>
      <p><strong>Videos:</strong> {channelStats.video_count}</p>
      <p><strong>Views:</strong> {channelStats.view_count}</p>

      {subscriberChartData && (
        <div className="subscriber-chart-toggle">
          <button onClick={toggleChart} className="toggle-button">
            {showChart ? 'Hide Subscriber Graph ▲' : 'Show Subscriber Graph ▼'}
          </button>
          {showChart && (
            <div className="subscriber-chart">
              <h4>Subscriber Growth</h4>
              <Line data={subscriberChartData} />
            </div>
          )}
        </div>
      )}

      {channelStats.videos && channelStats.videos.length > 0 && (
        <div className="channel-videos">
          <h3>Recent Videos</h3>
          <div className="video-list">
            {channelStats.videos.map((video) => (
              <div key={video.video_id} className="video-item">
                <a href={`https://www.youtube.com/watch?v=${video.video_id}`} target="_blank" rel="noopener noreferrer">
                  <img src={video.thumbnail} alt={video.title} />
                  <p>{video.title}</p>
                </a>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ChannelStatsCard;