import React from "react";

function Footer({ htmlContent, handleAbout }) {
  return (
    <footer className="app-footer">
      <p>
        &copy;{" "}
        <strong>2025 Dipsankar Sinha, Nadeem Khan & Hrithik Roy</strong>{" "}
      </p>
      <div className="footer-links">
        <a href="/terms">Terms</a>
        <a href="/about" onClick={(event) => handleAbout(event)}>
          About
        </a>
        <a href="/contact">Contact</a>
        <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
      </div>
    </footer>
  );
}

export default Footer;
