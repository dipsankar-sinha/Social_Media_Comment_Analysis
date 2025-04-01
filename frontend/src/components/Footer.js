import React from "react";

function Footer({ htmlContent, handleAbout, handleContact }) {
  return (
    <footer className="app-footer">
      <p>
        &copy;{" "}
        <strong>2025 Dipsankar Sinha, Nadeem Khan & Hrithik Roy</strong>{" "}
      </p>
      <div className="footer-links">
        <a href="/about" onClick={(event) => handleAbout(event)}>
          About
        </a>
        <a href="/contact" onClick={(event) => handleContact(event)}>
          Contact
        </a>
      </div>
    </footer>
  );
}

export default Footer;
