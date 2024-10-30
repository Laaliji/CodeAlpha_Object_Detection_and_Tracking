// Import the TypingEffect component
import TypingEffect from 'react-typing-effect';
import './LandingPage.css'; // Importing the CSS file
import ImageUpload from './ImageUpload';

const LandingPage = () => {
  return (
    <div className="landing-container">
      <div
        className="background-overlay"
        style={{ backgroundImage: 'url(/playground.jpg)' }}
      />

      <div className="overlay-left" />
      <div className="overlay-right" />

      <nav className="navbar">
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#services">Services</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </nav>

      <div className="content-wrapper">
        <div className="main-content">
          <h1 className="title">
            <TypingEffect
              text={["Welcome to Object Detection and Tracking App"]}
              speed={20}
              eraseSpeed={20}
              typingDelay={500}
              eraseDelay={1000}
            />
          </h1>
          <span className="start-demo-text">Start Demo</span>
        </div>
      </div>

      <footer className="footer">
        <p>© developed by Zakariae LAALIJI @CodeAlpha</p>
      </footer>
    </div>
  );
};

export default LandingPage;

