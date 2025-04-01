import React from "react";
import dipImage from "../assets/Dipsankar_pic.png";
import nadeemImage from "../assets/Nadeem_pic.png";
function Contact() {
  return (
    <div className="result-panel">
      <h2>Contact Information</h2>
      <div className={"contacts-container"}>
        <div className="contact-card">
          <img src={dipImage} alt={"Dipsankar Sinha"} />
          <div>
            <h3>Dipsankar Sinha</h3>
            <p>KIIT University, India</p>
            <a
              href={"https://github.com/dipsankar-sinha"}
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </a>
            <a href={"https://www.linkedin.com/in/dipsankar-sinha-77013627a"}>
              LinkedIn
            </a>
          </div>
        </div>
        <div className="contact-card">
          <img src={nadeemImage} alt={"Nadeem Khan"} />
          <div>
            <h3>Nadeem Khan</h3>
            <p>KIIT University, India</p>
            <a
              href={"https://github.com/Nadeemkkhan"}
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </a>
            <a href={"https://www.linkedin.com/in/dipsankar-sinha-77013627a"}>
              LinkedIn
            </a>
          </div>
        </div>
        <div className="contact-card">
          <img src={"#"} alt={"Hrithik Roy"} />
          <div>
            <h3>Hrithik Roy</h3>
            <p>KIIT University, India</p>
            <a href={"https://github.com/the-roy123"}>GitHub</a>
            <a href={"https://www.linkedin.com/in/dipsankar-sinha-77013627a"}>
              LinkedIn
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Contact;
