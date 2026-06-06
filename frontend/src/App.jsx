import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [skills, setSkills] = useState([]);
  const [storedQuestions, setStoredQuestions] = useState([]);
  const [aiQuestions, setAiQuestions] = useState([]);
  const [selectedQuestion, setSelectedQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a resume");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      console.log(response.data);

      setSkills(response.data.skills || []);

      setStoredQuestions(
        response.data.stored_questions || []
      );

      setAiQuestions(
        response.data.ai_questions
          ?.split("\n")
          .filter((q) => q.trim() !== "") || []
      );

      alert("Resume Uploaded Successfully!");
    } catch (error) {
      console.error(error);
      alert("Upload Failed");
    }
  };
    const evaluateAnswer = async () => {

  if (!selectedQuestion) {
    alert("Select a question");
    return;
  }

  if (!answer.trim()) {
    alert("Enter your answer");
    return;
  }

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

    setFeedback(
      "Unable to evaluate answer."
    );
  }
};


  return (
    <div style={{ padding: "50px" }}>
      <h1>AI Interview Preparation System</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <br />
        <br />

        <button type="submit">
          Upload Resume
        </button>
      </form>

      <hr />

      <h2>Detected Skills</h2>

      <ul>
        {skills.map((skill, index) => (
          <li key={index}>{skill}</li>
        ))}
      </ul>

      <h2>Standard Interview Questions</h2>

      <ul>
        {storedQuestions.map((question, index) => (
          <li key={index}>{question}</li>
        ))}
      </ul>

      <h2>AI Generated Questions</h2>

      <ul>
        {aiQuestions.map((question, index) => (
          <li key={index}>{question}</li>
        ))}
      </ul>
      <hr />

    <h2>Practice Answer</h2>

      <select
        value={selectedQuestion}
        onChange={(e) => setSelectedQuestion(e.target.value)}
      >
      <option value="">Select a Question</option>

        {storedQuestions.map((q, index) => (
          <option key={index} value={q}>
         {q}
      </option>
   ))}

      {aiQuestions.map((q, index) => (
        <option key={`ai-${index}`} value={q}>
        {q}
        </option>
      ))}
    </select>

    <br/>
    <br/>

    <textarea
      rows="8"
      cols="80"
      placeholder="Type your answer here..."
      value={answer}
     onChange={(e) => setAnswer(e.target.value)}
    />

    <br />
    <br />

    <button onClick={evaluateAnswer}>
        Evaluate Answer
    </button>

<h2>Feedback</h2>

<pre>{feedback}</pre>
    </div>
  );
}

export default App;