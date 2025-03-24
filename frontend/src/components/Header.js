import React from 'react';

function Header({ resetState, handleTopListsClick }) {
  return (
    <header className="app-header futuristic-header">
      <div className="logo">Comment Analysis</div>
      <div className="search-bar">
        <input type="text" placeholder="Search..." />
        <button>Search</button>
      </div>
      <nav>
        <button onClick={resetState} className="nav-button">Home</button>
        <button onClick={handleTopListsClick} className="nav-button">Top Lists</button>
        <a href="/resources" className="nav-link">Resources</a>
        <a href="/login" className="nav-link">Login</a>
      </nav>
    </header>
  );
}

export default Header;