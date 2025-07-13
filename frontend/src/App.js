import React, { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [contactForm, setContactForm] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [submitStatus, setSubmitStatus] = useState('');

  // Hero Section with professional layout
  const HeroSection = () => (
    <section className="hero-section">
      <div className="hero-overlay">
        <div className="hero-container">
          <div className="hero-left">
            <div className="profile-picture-area">
              <div className="profile-placeholder">
                <span className="profile-initials">DM</span>
              </div>
              <div className="profile-ring"></div>
            </div>
          </div>
          <div className="hero-right">
            <div className="hero-content">
              <h1 className="hero-name">DHANYASHREE M V</h1>
              <h2 className="hero-title">AI/ML Engineering Student</h2>
              <p className="hero-tagline">
                Building intelligent, user-focused solutions through code and creativity
              </p>
              <div className="hero-details">
                <div className="detail-item">
                  <span className="detail-icon">📍</span>
                  <span>Bengaluru, Karnataka</span>
                </div>
                <div className="detail-item">
                  <span className="detail-icon">📧</span>
                  <span>dhanyashreem@gmail.com</span>
                </div>
                <div className="detail-item">
                  <span className="detail-icon">📱</span>
                  <span>+91 8860769397</span>
                </div>
              </div>
              <div className="hero-stats">
                <div className="stat-item">
                  <span className="stat-number">4+</span>
                  <span className="stat-label">Projects</span>
                </div>
                <div className="stat-item">
                  <span className="stat-number">6+</span>
                  <span className="stat-label">Technologies</span>
                </div>
                <div className="stat-item">
                  <span className="stat-number">2</span>
                  <span className="stat-label">Leadership Roles</span>
                </div>
              </div>
              <div className="hero-links">
                <a href="https://www.linkedin.com/in/dhanyashree-mv-27d/" target="_blank" rel="noopener noreferrer" className="social-link">
                  <span className="social-icon">💼</span>
                  LinkedIn
                </a>
                <a href="https://github.com/DHANYASHREE-MV" target="_blank" rel="noopener noreferrer" className="social-link">
                  <span className="social-icon">💻</span>
                  GitHub
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );

  // About Section
  const AboutSection = () => (
    <section className="about-section">
      <div className="container">
        <div className="about-content">
          <div className="about-text">
            <h2 className="section-title">About Me</h2>
            <p className="about-description">
              Enthusiastic AI/ML engineering student exploring roles in software development and AI, 
              driven to build intelligent, user-focused solutions through code and creativity. 
              Passionate about leveraging technology to solve real-world problems and make a positive impact.
            </p>
            <div className="about-highlights">
              <div className="highlight-item">
                <span className="highlight-number">4+</span>
                <span className="highlight-text">Major Projects</span>
              </div>
              <div className="highlight-item">
                <span className="highlight-number">2</span>
                <span className="highlight-text">Leadership Roles</span>
              </div>
              <div className="highlight-item">
                <span className="highlight-number">6+</span>
                <span className="highlight-text">Technologies</span>
              </div>
            </div>
          </div>
          <div className="about-image">
            <img src="https://images.unsplash.com/photo-1717501218385-55bc3a95be94?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlfGVufDB8fHxwdXJwbGV8MTc1MjM5ODk1NXww&ixlib=rb-4.1.0&q=85" alt="AI Visualization" />
          </div>
        </div>
      </div>
    </section>
  );

  // Education Section
  const EducationSection = () => (
    <section className="education-section">
      <div className="container">
        <h2 className="section-title">Education</h2>
        <div className="education-timeline">
          <div className="education-item">
            <div className="education-year">2022 - 2026</div>
            <div className="education-content">
              <h3>Bachelor of Engineering</h3>
              <h4>Dayananda Sagar College Of Engineering</h4>
              <p>Branch: Artificial Intelligence and Machine Learning</p>
            </div>
          </div>
          <div className="education-item">
            <div className="education-year">2020 - 2022</div>
            <div className="education-content">
              <h3>Pre-University Course</h3>
              <h4>MES PU College</h4>
              <p>Branch: Science PCMB</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );

  // Skills Section
  const SkillsSection = () => (
    <section className="skills-section">
      <div className="container">
        <h2 className="section-title">Skills & Technologies</h2>
        <div className="skills-grid">
          <div className="skill-category">
            <h3>Technical Skills</h3>
            <div className="skills-list">
              {['NumPy', 'Pandas', 'PyTorch', 'TensorFlow', 'Keras', 'Sklearn', 'Docker', 'Matlab', 'Tableau'].map(skill => (
                <span key={skill} className="skill-tag">{skill}</span>
              ))}
            </div>
          </div>
          <div className="skill-category">
            <h3>Programming Languages</h3>
            <div className="skills-list">
              {['Python', 'R', 'C', 'JavaScript', 'HTML', 'CSS'].map(skill => (
                <span key={skill} className="skill-tag">{skill}</span>
              ))}
            </div>
          </div>
          <div className="skill-category">
            <h3>Soft Skills</h3>
            <div className="skills-list">
              {['Problem Solving', 'Teamwork', 'Adaptability', 'Time Management', 'Communication'].map(skill => (
                <span key={skill} className="skill-tag">{skill}</span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );

  // Experience Section
  const ExperienceSection = () => (
    <section className="experience-section">
      <div className="container">
        <h2 className="section-title">Experience</h2>
        <div className="experience-timeline">
          <div className="experience-item">
            <div className="experience-year">2025</div>
            <div className="experience-content">
              <h3>Co-Lead Content Team</h3>
              <h4>The Central Committee - DSCE</h4>
              <ul>
                <li>Spearheaded content strategy and editorial management for consistent, impactful messaging</li>
                <li>Coordinated team efforts to deliver high-quality communications aligned with organizational goals</li>
              </ul>
            </div>
          </div>
          <div className="experience-item">
            <div className="experience-year">2023</div>
            <div className="experience-content">
              <h3>Event Management Volunteer</h3>
              <h4>E-Summit - IEDC</h4>
              <ul>
                <li>Assisted in planning and coordinating event activities for seamless execution</li>
                <li>Supported participant engagement to enhance overall event experience</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );

  // Projects Section
  const ProjectsSection = () => (
    <section className="projects-section">
      <div className="container">
        <h2 className="section-title">Featured Projects</h2>
        <div className="projects-grid">
          <div className="project-card">
            <div className="project-image">
              <img src="https://images.pexels.com/photos/8728386/pexels-photo-8728386.jpeg" alt="IoT Project" />
            </div>
            <div className="project-content">
              <h3>PURE FLOW</h3>
              <p className="project-subtitle">IoT-Based Water Quality Monitoring System</p>
              <p>Designed and implemented an Arduino ESP32 system equipped with multiple sensors to perform real-time water quality monitoring, capturing parameters like pH, turbidity, and temperature. Integrated cloud connectivity and IoT visualization by linking the system to the Blynk platform, enabling remote data access, live monitoring, and real-time alerts.</p>
            </div>
          </div>
          
          <div className="project-card">
            <div className="project-content">
              <h3>DIAGNO-GENIE</h3>
              <p className="project-subtitle">Machine Learning Multiple Disease Prediction System</p>
              <p>Built a web-based Multiple Disease Prediction System using machine learning to predict Diabetes, Heart Disease, and Parkinson's Disease from user input. Developed ML pipelines for training and evaluation, with integrated experiment tracking and artifact logging via MLflow. The application features an interactive Streamlit interface, automated model reporting, and Docker-based deployment for portability.</p>
            </div>
          </div>

          <div className="project-card">
            <div className="project-content">
              <h3>WILD GUARD AI</h3>
              <p className="project-subtitle">Deep Learning + Computer Vision</p>
              <p>Developed a real-time wildlife monitoring system using YOLOv11 for detecting poachers, rangers, and tourists from camera images. Integrated a Streamlit-based frontend to support real-time image uploads and display detection results in an interactive, scrollable layout. Implemented automated SMS alerts via Twilio API to notify authorities instantly when poachers are detected.</p>
            </div>
          </div>

          <div className="project-card">
            <div className="project-content">
              <h3>OZONE LEVEL FORECASTING</h3>
              <p className="project-subtitle">Air Quality Visualization System</p>
              <p>Developed a deep learning-based ozone forecasting system using LSTM models to predict monthly ozone levels from 2024 to 2027 across seven major locations in Bangalore, aimed at improving air quality insights and supporting public health awareness initiatives. The project leveraged Python, TensorFlow, Keras, Pandas, NumPy, Matplotlib, Seaborn, and Streamlit, with all data processed from structured CSV files for multi-location forecasting.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );

  // Leadership & Extra-curricular Section
  const LeadershipSection = () => (
    <section className="leadership-section">
      <div className="container">
        <h2 className="section-title">Leadership & Extra-curricular</h2>
        <div className="leadership-content">
          <div className="leadership-item">
            <h3>Leadership</h3>
            <p>Co-led the content team, overseeing strategy, creation, and quality control across multiple platforms. Collaborated with cross-functional teams to ensure consistent, engaging, and impactful communication.</p>
          </div>
          <div className="activities-item">
            <h3>Extra-curricular Activities</h3>
            <div className="activities-list">
              <span className="activity-tag">Blog Writing</span>
              <span className="activity-tag">Coding</span>
              <span className="activity-tag">Developing</span>
              <span className="activity-tag">Dancing</span>
              <span className="activity-tag">Binge-watching</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );

  // Contact Section
  const ContactSection = () => {
    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        setSubmitStatus('Sending...');
        const response = await axios.post(`${API}/contact`, contactForm);
        setSubmitStatus('Message sent successfully!');
        setContactForm({ name: '', email: '', message: '' });
        setTimeout(() => setSubmitStatus(''), 3000);
      } catch (error) {
        setSubmitStatus('Error sending message. Please try again.');
        setTimeout(() => setSubmitStatus(''), 3000);
      }
    };

    const handleChange = (e) => {
      setContactForm({
        ...contactForm,
        [e.target.name]: e.target.value
      });
    };

    return (
      <section className="contact-section">
        <div className="container">
          <h2 className="section-title">Get In Touch</h2>
          <div className="contact-content">
            <div className="contact-info">
              <h3>Let's Connect</h3>
              <p>I'm always open to discussing new opportunities, collaborations, or just having a conversation about technology and AI.</p>
              <div className="contact-details">
                <div className="contact-item">
                  <span className="contact-icon">📧</span>
                  <span>dhanyashreem@gmail.com</span>
                </div>
                <div className="contact-item">
                  <span className="contact-icon">📱</span>
                  <span>+91 8860769397</span>
                </div>
                <div className="contact-item">
                  <span className="contact-icon">📍</span>
                  <span>Bengaluru, Karnataka</span>
                </div>
              </div>
              <div className="social-links">
                <a href="https://www.linkedin.com/in/dhanyashree-mv-27d/" target="_blank" rel="noopener noreferrer" className="social-link">LinkedIn</a>
                <a href="https://github.com/DHANYASHREE-MV" target="_blank" rel="noopener noreferrer" className="social-link">GitHub</a>
              </div>
            </div>
            <form className="contact-form" onSubmit={handleSubmit}>
              <input
                type="text"
                name="name"
                placeholder="Your Name"
                value={contactForm.name}
                onChange={handleChange}
                required
              />
              <input
                type="email"
                name="email"
                placeholder="Your Email"
                value={contactForm.email}
                onChange={handleChange}
                required
              />
              <textarea
                name="message"
                placeholder="Your Message"
                rows="5"
                value={contactForm.message}
                onChange={handleChange}
                required
              ></textarea>
              <button type="submit" className="submit-btn">Send Message</button>
              {submitStatus && <p className="submit-status">{submitStatus}</p>}
            </form>
          </div>
        </div>
      </section>
    );
  };

  return (
    <div className="App">
      <HeroSection />
      <AboutSection />
      <EducationSection />
      <SkillsSection />
      <ExperienceSection />
      <ProjectsSection />
      <LeadershipSection />
      <ContactSection />
    </div>
  );
}

export default App;