import React, { useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
);

const ChannelStatsCard = ({
  channelStats,
  subscriberChartData,
  maxResults,
  setMaxResults,
  handleVideoCommentAnalysis,
}) => {
  const [showChart, setShowChart] = useState(false);

  const toggleChart = () => {
    setShowChart((prev) => !prev);
  };

  return (
    <div className="channel-stats-card">
      <h3>Channel Statistics</h3>
      <p>
        <strong>Channel ID:</strong> {channelStats.channel_id}
      </p>
      <p>
        <strong>Title:</strong> {channelStats.title}
      </p>
      <p>
        <strong>Description:</strong> {channelStats.description}
      </p>
      <p>
        <strong>Subscribers:</strong> {channelStats.subscriber_count || "N/A"}
      </p>
      <p>
        <strong>Videos:</strong> {channelStats.video_count}
      </p>
      <p>
        <strong>Views:</strong> {channelStats.view_count}
      </p>

      {subscriberChartData && (
        <div className="subscriber-chart-toggle">
          <button onClick={toggleChart} className="btn">
            {showChart ? "Hide Subscriber Graph ▲" : "Show Subscriber Graph ▼"}
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
        <div className="result-card">
          <h3>Recent Videos</h3>
          <div className="video-list">
            {channelStats.videos.map((video) => (
              <div key={video.video_id} className="youtube-videos-card">
                <img src={video.thumbnail.high.url} alt={video.title} />
                <div>
                  <h4>{video.title}</h4>
                  <a
                    href={`https://www.youtube.com/watch?v=${video.video_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Watch on YouTube
                  </a>
                  <label>
                    Select No. Of Comments:
                    <input
                      type="number"
                      placeholder="Max Results (default 10)"
                      value={maxResults}
                      onChange={(e) => setMaxResults(Number(e.target.value))}
                    />
                  </label>
                  <button
                    className="btn"
                    onClick={() => {
                      //setVideoID(video.id); // Update the video ID state
                      handleVideoCommentAnalysis(video.video_id); // Trigger the comment analysis function
                    }}
                  >
                    Analyze Video Comments
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ChannelStatsCard;
