import React from "react";

function Header({ resetState, handleTopListsClick }) {
  return (
    <header className="app-header futuristic-header">
      <div className="logo">Social Media Comment Analysis System</div>
      <nav>
        <button onClick={resetState} className="nav-button">
          Home
        </button>
        <button onClick={handleTopListsClick} className="nav-button">
          Top Lists
        </button>
      </nav>
    </header>
  );
}

export default Header;
