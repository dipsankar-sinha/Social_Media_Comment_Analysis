import React from 'react';

function Footer({htmlContent, handleAboutUs}) {
    return (
    <footer className="app-footer">
      <p>&copy; <strong>2025 Dipsankar Sinha, Nadeem Khan & Hrithik Roy</strong> </p>
      <div className="footer-links">
        <a href="/terms">Terms</a>
        <a
            href="/aboutus"
            onClick={(event) => handleAboutUs(event)}
        >
            About Us
        </a>
        <a href="/contact">Contact</a>
          <div
            dangerouslySetInnerHTML={{ __html: htmlContent }}
          />
      </div>
    </footer>
  );
}

export default Footer;