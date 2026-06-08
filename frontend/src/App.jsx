import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

// SVG Icons as inline components for robustness and zero dependencies
const SunIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
);

const MoonIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
);

const UploadCloudIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M12 12v9"/><path d="m15 15-3-3-3 3"/></svg>
);

const FileIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>
);

const TrashIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
);

const ShieldCheckIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 9.7a1 1 0 0 1-.68 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 .76-.97l8-2a1 1 0 0 1 .48 0l8 2A1 1 0 0 1 20 6v7z"/><path d="m9 12 2 2 4-4"/></svg>
);

const StarIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
);

const TrophyIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.45 1-1 1H4v2h16v-2h-5c-.55 0-1-.45-1-1v-2.34"/><path d="M12 2a6 6 0 0 1 6 6v5a6 6 0 0 1-6 6 6 6 0 0 1-6-6V8a6 6 0 0 1 6-6z"/></svg>
);

const BookOpenIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
);

const UserCheckIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/><path d="m16 11 2 2 4-4"/></svg>
);

const ClipboardIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/></svg>
);

const AlertTriangleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
);

function App() {
  const [file, setFile] = useState(null);
  const [skills, setSkills] = useState([]);
  const [storedQuestions, setStoredQuestions] = useState([]);
  const [aiQuestions, setAiQuestions] = useState([]);
  const [selectedQuestion, setSelectedQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  
  // Custom interactive layout states
  const [isDragOver, setIsDragOver] = useState(false);
  const [activeTab, setActiveTab] = useState("standard");
  const [isUploading, setIsUploading] = useState(false);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [isAiFallback, setIsAiFallback] = useState(false);
  
  // Theme state
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("theme") || "light";
  });

  useEffect(() => {
    const root = document.documentElement;
    if (theme === "dark") {
      root.classList.add("dark-theme");
      root.classList.remove("light-theme");
    } else {
      root.classList.add("light-theme");
      root.classList.remove("dark-theme");
    }
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  // Helper helper to strip numbered prefixes (e.g. "1. What is...") from Gemini
  const cleanQuestionText = (q) => {
    return q.replace(/^\d+[\.\)]\s*/, "").replace(/^[-*]\s*/, "").trim();
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === "application/pdf") {
        setFile(droppedFile);
      } else {
        alert("Please drop a valid PDF file.");
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const removeFile = () => {
    setFile(null);
    setSkills([]);
    setStoredQuestions([]);
    setAiQuestions([]);
    setSelectedQuestion("");
    setAnswer("");
    setFeedback("");
    setIsAiFallback(false);
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();

    if (!file) {
      alert("Please select a resume");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    setIsUploading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      setSkills(response.data.skills || []);
      setStoredQuestions(response.data.stored_questions || []);
      setIsAiFallback(response.data.is_ai_fallback || false);

      // Filter and clean AI questions
      let rawAi = response.data.ai_questions || "";
      let cleanedQuestions = [];
      if (typeof rawAi === "string") {
        cleanedQuestions = rawAi
          .split("\n")
          .filter((q) => q.trim() !== "")
          .map(cleanQuestionText);
      } else if (Array.isArray(rawAi)) {
        cleanedQuestions = rawAi.map(cleanQuestionText);
      }
      setAiQuestions(cleanedQuestions);

      // Default active tab preference based on standard list presence
      if (response.data.stored_questions?.length === 0 && cleanedQuestions.length > 0) {
        setActiveTab("ai");
      } else {
        setActiveTab("standard");
      }
      
    } catch (error) {
      console.error(error);
      alert("Upload Failed. Please ensure the backend is running at http://127.0.0.1:8000");
    } finally {
      setIsUploading(false);
    }
  };

  const evaluateAnswer = async () => {
    if (!selectedQuestion) {
      alert("Please select a question to practice.");
      return;
    }

    if (!answer.trim()) {
      alert("Please type your answer before submitting.");
      return;
    }

    setIsEvaluating(true);
    setFeedback("");

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/evaluate",
        {
          question: selectedQuestion,
          answer: answer
        }
      );
      setFeedback(response.data.feedback);
    } catch (error) {
      console.error(error);
      setFeedback("Unable to evaluate answer. Please verify connection to the server.");
    } finally {
      setIsEvaluating(false);
    }
  };

  // Structured Feedback Parser
  const parseFeedback = (rawText) => {
    if (!rawText) return null;

    let score = "0/10";
    let strengths = [];
    let improvements = [];
    let isFallback = false;

    // Check if evaluator output is standard format
    const lines = rawText.split("\n").map((line) => line.trim()).filter(Boolean);
    let currentSection = ""; // "strengths" or "improvements"

    for (const line of lines) {
      const lowerLine = line.toLowerCase();
      
      if (lowerLine.startsWith("score:")) {
        score = line.replace(/score:\s*/i, "").trim();
        continue;
      }
      
      if (lowerLine.startsWith("strengths:")) {
        currentSection = "strengths";
        continue;
      }
      
      if (lowerLine.startsWith("improvements:")) {
        currentSection = "improvements";
        continue;
      }

      // Match bullets like "-", "*", or digits
      if (line.startsWith("-") || line.startsWith("*") || /^\d+\./.test(line)) {
        const bulletContent = line.replace(/^[-*\d.]+\s*/, "").trim();
        if (currentSection === "strengths") {
          strengths.push(bulletContent);
        } else if (currentSection === "improvements") {
          improvements.push(bulletContent);
        }
      } else if (currentSection) {
        if (currentSection === "strengths") {
          strengths.push(line);
        } else if (currentSection === "improvements") {
          improvements.push(line);
        }
      }
    }

    // Determine fallback values if structure was not recognized
    if (strengths.length === 0 && improvements.length === 0) {
      isFallback = true;
    }

    return { score, strengths, improvements, isFallback };
  };

  const parsedFeedback = parseFeedback(feedback);

  // Statistics values
  const totalQuestions = storedQuestions.length + aiQuestions.length;
  
  // Word & character counts
  const wordCount = answer.trim() === "" ? 0 : answer.trim().split(/\s+/).length;
  const charCount = answer.length;

  return (
    <div className="app-container">
      {/* Top Header Bar */}
      <header className="header">
        <div className="brand">
          <div className="logo-icon">P</div>
          <div className="brand-details">
            <h1>PrepAI</h1>
            <p>Adaptive Technical Interview Simulator</p>
          </div>
        </div>
        <div className="header-actions">
          <button 
            className="theme-toggle" 
            onClick={toggleTheme} 
            title={theme === "light" ? "Switch to Dark Mode" : "Switch to Light Mode"}
            aria-label="Toggle Theme"
          >
            {theme === "light" ? <MoonIcon /> : <SunIcon />}
          </button>
        </div>
      </header>

      {/* Hero Intro */}
      <section className="hero">
        <span className="badge-tag">Platform Version 2.0</span>
        <h2>Master Your Next Technical Interview</h2>
        <p>
          Upload your resume in PDF format. We will scan your skillset, generate a
          tailored interview deck, and evaluate your responses with real-time AI metrics.
        </p>
      </section>

      {/* Portal Stats Bar */}
      <section className="stats-bar">
        <div className="stat-card">
          <div className="stat-icon"><TrophyIcon /></div>
          <div className="stat-info">
            <span className="stat-value">94%</span>
            <span className="stat-label">Average Accuracy</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon"><BookOpenIcon /></div>
          <div className="stat-info">
            <span className="stat-value">{skills.length || "-"}</span>
            <span className="stat-label">Skills Extracted</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon"><UserCheckIcon /></div>
          <div className="stat-info">
            <span className="stat-value">{totalQuestions || "-"}</span>
            <span className="stat-label">Tailored Questions</span>
          </div>
        </div>
      </section>

      {/* Main Grid Workspace */}
      <div className="dashboard-grid">
        
        {/* Left Hand Column: Inputs & Custom Settings */}
        <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
          
          {/* Card 1: Resume PDF Uploader */}
          <div className={`card ${!file ? "active-step" : ""}`}>
            <div className="card-header">
              <span className="card-step">Step 1</span>
              <h3 className="card-title">Resume Upload</h3>
              <p className="card-desc">Provide your PDF resume to load candidate settings</p>
            </div>
            
            <div className="upload-container">
              {!file ? (
                <div 
                  className={`dropzone ${isDragOver ? "active" : ""}`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => document.getElementById("resume-input").click()}
                >
                  <input
                    type="file"
                    id="resume-input"
                    accept=".pdf"
                    style={{ display: "none" }}
                    onChange={handleFileChange}
                  />
                  <div className="upload-icon"><UploadCloudIcon /></div>
                  <span className="upload-text">Drag & drop your PDF or click to browse</span>
                  <span className="upload-hint">Supports PDF up to 10MB</span>
                </div>
              ) : (
                <div className="file-info animate-fade-in">
                  <div className="file-details">
                    <span className="file-icon"><FileIcon /></span>
                    <div>
                      <div style={{ fontWeight: 600, color: "var(--text-main)", overflow: "hidden", textOverflow: "ellipsis", maxWidth: "200px", whiteSpace: "nowrap" }}>
                        {file.name}
                      </div>
                      <div style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                        {(file.size / 1024).toFixed(1)} KB
                      </div>
                    </div>
                  </div>
                  <button className="remove-file-btn" onClick={removeFile} title="Remove file">
                    <TrashIcon />
                  </button>
                </div>
              )}

              {file && skills.length === 0 && (
                <button 
                  className="btn btn-primary" 
                  disabled={isUploading}
                  onClick={handleSubmit}
                  style={{ width: "100%" }}
                >
                  {isUploading ? (
                    <>
                      <span className="spinner"></span>
                      Scanning Resume...
                    </>
                  ) : (
                    "Process & Generate Questions"
                  )}
                </button>
              )}
            </div>
          </div>

          {/* Card 2: Extracted Skills */}
          {file && (
            <div className="card">
              <div className="card-header">
                <span className="card-step">Step 2</span>
                <h3 className="card-title">Extracted Skill Profiles</h3>
                <p className="card-desc">Recognized competencies mapped from your resume</p>
              </div>

              {isUploading ? (
                <div className="empty-state">
                  <span className="spinner spinner-primary" style={{ width: "24px", height: "24px" }}></span>
                  <p>Processing skills...</p>
                </div>
              ) : skills.length > 0 ? (
                <div className="skills-container animate-fade-in">
                  {skills.map((skill, index) => (
                    <span key={index} className="skill-badge">
                      <span style={{ width: "6px", height: "6px", borderRadius: "50%", background: "var(--primary)" }}></span>
                      {skill.toUpperCase()}
                    </span>
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  <p>No matches yet. Awaiting resume scan details.</p>
                </div>
              )}
            </div>
          )}

          {/* Card 3: Question Hub Selector */}
          {file && (skills.length > 0 || aiQuestions.length > 0) && (
            <div className={`card ${!selectedQuestion ? "active-step" : ""}`}>
              <div className="card-header">
                <span className="card-step">Step 3</span>
                <h3 className="card-title">Interview Question Banks</h3>
                <p className="card-desc">Select a question below to load it into the response terminal</p>
              </div>

              <div className="tabs-header">
                <button 
                  className={`tab-btn ${activeTab === "standard" ? "active" : ""}`}
                  onClick={() => setActiveTab("standard")}
                >
                  Core Questions ({storedQuestions.length})
                </button>
                <button 
                  className={`tab-btn ${activeTab === "ai" ? "active" : ""}`}
                  onClick={() => setActiveTab("ai")}
                >
                  AI Generated ({aiQuestions.length})
                </button>
              </div>

              <div className="question-list animate-fade-in">
                {activeTab === "standard" ? (
                  storedQuestions.length > 0 ? (
                    storedQuestions.map((q, index) => (
                      <div 
                        key={index} 
                        className={`question-item ${selectedQuestion === q ? "selected" : ""}`}
                        onClick={() => setSelectedQuestion(q)}
                      >
                        <div className="radio-indicator"></div>
                        <div className="question-text">{q}</div>
                      </div>
                    ))
                  ) : (
                    <div className="empty-state"><p>No core questions for the detected skills.</p></div>
                  )
                ) : (
                  <>
                    {isAiFallback && (
                      <div style={{
                        background: "var(--warning-light)",
                        color: "var(--warning)",
                        fontSize: "0.85rem",
                        padding: "0.75rem 1rem",
                        borderRadius: "var(--radius-md)",
                        border: "1px solid var(--border)",
                        marginBottom: "0.75rem",
                        display: "flex",
                        gap: "0.5rem",
                        alignItems: "center",
                        fontWeight: 500,
                        textAlign: "left"
                      }}>
                        <span style={{ fontSize: "1.2rem", flexShrink: 0 }}>⚠️</span>
                        <span>AI API is currently unavailable (rate-limited or key missing). Loaded high-quality technical fallback questions.</span>
                      </div>
                    )}
                    {aiQuestions.length > 0 ? (
                      aiQuestions.map((q, index) => (
                        <div 
                          key={`ai-${index}`} 
                          className={`question-item ${selectedQuestion === q ? "selected" : ""}`}
                          onClick={() => setSelectedQuestion(q)}
                        >
                          <div className="radio-indicator"></div>
                          <div className="question-text">{q}</div>
                        </div>
                      ))
                    ) : (
                      <div className="empty-state"><p>No custom AI questions generated.</p></div>
                    )}
                  </>
                )}
              </div>
            </div>
          )}

        </div>

        {/* Right Hand Column: Sandbox simulator & Scorecard Feedback */}
        <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
          
          {/* Card 4: Answer sandbox playground */}
          <div className={`card ${selectedQuestion && !feedback ? "active-step" : ""}`}>
            <div className="card-header">
              <span className="card-step">Step 4</span>
              <h3 className="card-title">Practice Sandbox</h3>
              <p className="card-desc">Type your answer. Aim for structured, comprehensive replies.</p>
            </div>

            {selectedQuestion ? (
              <div className="sandbox-container animate-fade-in">
                <div className="selected-question-banner">
                  <div style={{ fontSize: "0.75rem", fontWeight: 700, textTransform: "uppercase", color: "var(--primary)", marginBottom: "0.25rem" }}>
                    Selected Question:
                  </div>
                  {selectedQuestion}
                </div>

                <textarea
                  className="answer-textarea"
                  placeholder="Draft your answer details here. Use code concepts, design patterns, or structured algorithms in your explanation..."
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  disabled={isEvaluating}
                />

                <div className="sandbox-meta">
                  <div className="word-count">
                    <span><strong>Words:</strong> {wordCount}</span>
                    <span><strong>Characters:</strong> {charCount}</span>
                  </div>
                  <span style={{ fontSize: "0.75rem", color: wordCount < 20 ? "var(--warning)" : "var(--success)" }}>
                    {wordCount < 20 ? "💡 Add more depth for better score" : "✓ Great answer length"}
                  </span>
                </div>

                <div style={{ display: "flex", gap: "1rem" }}>
                  <button 
                    className="btn btn-primary" 
                    onClick={evaluateAnswer}
                    disabled={isEvaluating || !answer.trim()}
                    style={{ flex: 1 }}
                  >
                    {isEvaluating ? (
                      <>
                        <span className="spinner"></span>
                        AI Evaluation in Progress...
                      </>
                    ) : (
                      "Submit & Evaluate Answer"
                    )}
                  </button>
                  <button 
                    className="btn btn-secondary" 
                    onClick={() => setAnswer("")}
                    disabled={isEvaluating || !answer}
                  >
                    Reset Text
                  </button>
                </div>
              </div>
            ) : (
              <div className="no-question-selected">
                <div style={{ fontSize: "2rem" }}>🎙️</div>
                <p>Select a question from the bank to start simulated sandbox practice.</p>
              </div>
            )}
          </div>

          {/* Card 5: AI Feedback & Scorecard */}
          {(isEvaluating || feedback) && (
            <div className="card active-step">
              <div className="card-header">
                <span className="card-step">Step 5</span>
                <h3 className="card-title">AI Performance Analytics</h3>
                <p className="card-desc">Detailed feedback metrics and grading points compiled by PrepAI</p>
              </div>

              {isEvaluating ? (
                <div className="evaluating-card animate-fade-in">
                  <div className="large-spinner"></div>
                  <div>
                    <h4 style={{ fontWeight: 600, color: "var(--text-main)", marginBottom: "0.25rem" }}>Evaluating Responses...</h4>
                    <p style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>Analyzing vocabulary, correctness, and structural quality</p>
                  </div>
                </div>
              ) : parsedFeedback ? (
                <div className="evaluation-details animate-fade-in">
                  <div className="evaluation-header">
                    <div className="score-display">
                      <div className="score-radial">
                        {parsedFeedback.score.includes("/") ? parsedFeedback.score.split("/")[0] : parsedFeedback.score}
                      </div>
                      <div className="score-meta">
                        <h3>Overall Score</h3>
                        <p>Aggregated technical match scale</p>
                      </div>
                    </div>
                    <div>
                      {(() => {
                        const numScore = parseFloat(parsedFeedback.score);
                        if (!isNaN(numScore)) {
                          if (numScore >= 8) return <span className="score-badge high">Advanced</span>;
                          if (numScore >= 6) return <span className="score-badge mid">Intermediate</span>;
                          return <span className="score-badge low">Basic</span>;
                        }
                        return <span className="score-badge mid">Evaluated</span>;
                      })()}
                    </div>
                  </div>

                  {parsedFeedback.isFallback ? (
                    // Display raw text fallback if formatting is completely custom
                    <pre style={{
                      whiteSpace: "pre-wrap",
                      fontFamily: "var(--font-sans)",
                      fontSize: "0.85rem",
                      lineHeight: "1.5",
                      background: "var(--bg)",
                      padding: "1rem",
                      borderRadius: "var(--radius-md)",
                      border: "1px solid var(--border)",
                      color: "var(--text-main)"
                    }}>
                      {feedback}
                    </pre>
                  ) : (
                    // Beautiful styled sections
                    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
                      
                      {parsedFeedback.strengths.length > 0 && (
                        <div className="eval-card strengths">
                          <h4 className="eval-card-title">
                            <span className="eval-bullet"><ShieldCheckIcon /></span>
                            Candidate Strengths
                          </h4>
                          <ul className="eval-list">
                            {parsedFeedback.strengths.map((str, i) => (
                              <li key={i} className="eval-item">
                                <span style={{ color: "var(--success)" }}>✓</span>
                                {str}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {parsedFeedback.improvements.length > 0 && (
                        <div className="eval-card improvements">
                          <h4 className="eval-card-title">
                            <span className="eval-bullet"><AlertTriangleIcon /></span>
                            Areas for Improvement
                          </h4>
                          <ul className="eval-list">
                            {parsedFeedback.improvements.map((imp, i) => (
                              <li key={i} className="eval-item">
                                <span style={{ color: "var(--warning)" }}>•</span>
                                {imp}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}

                  <div style={{ display: "flex", justifyContent: "flex-end", gap: "1rem", marginTop: "0.5rem" }}>
                    <button 
                      className="btn btn-secondary" 
                      onClick={() => {
                        setFeedback("");
                        setAnswer("");
                      }}
                      style={{ fontSize: "0.85rem", padding: "0.5rem 1rem" }}
                    >
                      Clear Feedback
                    </button>
                  </div>
                </div>
              ) : null}
            </div>
          )}

        </div>

      </div>

      {/* Foot Footer */}
      <footer className="footer">
        <div>
          Designed for technical job seekers. Powered by Gemini LLM models.
        </div>
        <div>
          <span>© 2026 PrepAI Portal. </span>
          <a href="#" onClick={(e) => { e.preventDefault(); alert("PrepAI v2.0 - A premium student capstone project simulator."); }}>
            System Info
          </a>
        </div>
      </footer>
    </div>
  );
}

export default App;