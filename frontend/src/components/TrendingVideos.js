import React from 'react';

function TrendingVideos({ trendingVideos, maxResults, setMaxResults, handleVideoCommentAnalysis}) {
  return (
    <div className="right-panel">
      <h2>Trending YouTube Videos</h2>
      {trendingVideos.map((video) => (
        <div key={video.id} className="youtube-videos-card">
          <img src={video.snippet.thumbnails.maxres ? video.snippet.thumbnails.maxres.url : video.snippet.thumbnails.standard.url} alt={video.snippet.title} />
          <div>
            <h3>{video.snippet.title}</h3>
            <p>{video.snippet.description}</p>
            <a href={`https://www.youtube.com/watch?v=${video.id}`} target="_blank" rel="noopener noreferrer">Watch on YouTube</a>
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
                handleVideoCommentAnalysis(video.id); // Trigger the comment analysis function
              }}
            >
              Analyze Video Comments
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default TrendingVideos;