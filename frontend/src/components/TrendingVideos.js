import React from 'react';

function TrendingVideos({ trendingVideos }) {
  return (
    <div className="right-panel">
      <h2>Trending YouTube Videos</h2>
      {trendingVideos.map((video) => (
        <div key={video.id} className="trending-video-card">
          <img src={video.snippet.thumbnails.maxres ? video.snippet.thumbnails.maxres.url : video.snippet.thumbnails.standard.url} alt={video.snippet.title} />
          <h3>{video.snippet.title}</h3>
          <p>{video.snippet.description}</p>
          <a href={`https://www.youtube.com/watch?v=${video.id}`} target="_blank" rel="noopener noreferrer">Watch on YouTube</a>
        </div>
      ))}
    </div>
  );
}

export default TrendingVideos;