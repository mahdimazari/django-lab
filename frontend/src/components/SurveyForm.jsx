import React, { useState } from "react";
import { createSurvey } from "../utils/apiHelpers";

function SurveyForm() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [questions, setQuestions] = useState([]);

  const addQuestion = () => {
    setQuestions([
      ...questions,
      { text: "", question_type: "text", required: true, choices: [] },
    ]);
  };

  const updateQuestion = (index, key, value) => {
    const updatedQuestions = [...questions];
    updatedQuestions[index][key] = value;
    setQuestions(updatedQuestions);
  };

  const addChoice = (index) => {
    const updatedQuestions = [...questions];
    updatedQuestions[index].choices.push("");
    setQuestions(updatedQuestions);
  };

  const updateChoice = (questionIndex, choiceIndex, value) => {
    const updatedQuestions = [...questions];
    updatedQuestions[questionIndex].choices[choiceIndex] = value;
    setQuestions(updatedQuestions);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("test", title, description, questions);
    createSurvey({ title, description, questions })
      .then(() => {
        alert("Survey created successfully!");
      })
      .catch((error) => {
        console.error("Error creating survey:", error);
      });
  };

  return (
    <div>
      <h1>Create a Survey</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title:</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>
        <div>
          <label>Description:</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          ></textarea>
        </div>
        <h2>Questions</h2>
        {questions.map((question, index) => (
          <div key={index}>
            <label>Question Text:</label>
            <input
              type="text"
              value={question.text}
              onChange={(e) => updateQuestion(index, "text", e.target.value)}
            />
            <label>Question Type:</label>
            <select
              value={question.question_type}
              onChange={(e) =>
                updateQuestion(index, "question_type", e.target.value)
              }
            >
              <option value="text">Text</option>
              <option value="textarea">Textarea</option>
              <option value="radio">Radio</option>
              <option value="checkbox">Checkbox</option>
            </select>
            <label>Required:</label>
            <input
              type="checkbox"
              checked={question.required}
              onChange={(e) =>
                updateQuestion(index, "required", e.target.checked)
              }
            />
            {(question.question_type === "radio" ||
              question.question_type === "checkbox") && (
              <div>
                <h4>Choices</h4>
                {question.choices.map((choice, choiceIndex) => (
                  <div key={choiceIndex}>
                    <input
                      type="text"
                      value={choice}
                      onChange={(e) =>
                        updateChoice(index, choiceIndex, e.target.value)
                      }
                    />
                  </div>
                ))}
                <button type="button" onClick={() => addChoice(index)}>
                  Add Choice
                </button>
              </div>
            )}
          </div>
        ))}
        <button type="button" onClick={addQuestion}>
          Add Question
        </button>
        <button type="submit">Create Survey</button>
      </form>
    </div>
  );
}

export default SurveyForm;
