import React, { useEffect, useState } from "react";
// import axios from "axios";
import api from "../api";
import { useParams } from "react-router-dom";

const SurveyDetail = () => {
  // console.log("id", match);
  const { id } = useParams();
  const [survey, setSurvey] = useState(null);
  const [answers, setAnswers] = useState({});

  useEffect(() => {
    api.get(`/api/surveys/${id}/`).then((response) => {
      console.log("survey", response);
      setSurvey(response.data);
    });
  }, [id]);

  const handleSubmit = (e) => {
    e.preventDefault();
    api
      .post(`/api/surveys/${survey.id}/responses/`, {
        answers: Object.values(answers),
      })
      .then(() => {
        alert("Survey submitted successfully!");
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const handleAnswerChange = (questionId, value) => {
    setAnswers({
      ...answers,
      [questionId]: {
        question: questionId,
        text:
          survey.questions.find((q) => q.id === questionId).question_type ===
          "text"
            ? value
            : "",
        choice:
          survey.questions.find((q) => q.id === questionId).question_type !==
          "text"
            ? value
            : null,
      },
    });
  };

  if (!survey) return <p>Loading...</p>;

  return (
    <div>
      <h1>{survey.title}</h1>
      <p>{survey.description}</p>
      <form onSubmit={handleSubmit}>
        {survey.questions.map((question) => (
          <div key={question.id}>
            <p>{question.text}</p>
            {question.question_type === "text" && (
              <input
                type="text"
                onChange={(e) =>
                  handleAnswerChange(question.id, e.target.value)
                }
              />
            )}
            {question.question_type === "radio" &&
              question.choices.map((choice) => (
                <div key={choice.id}>
                  <input
                    type="radio"
                    name={`question_${question.id}`}
                    value={choice.id}
                    onChange={(e) =>
                      handleAnswerChange(question.id, e.target.value)
                    }
                  />
                  {choice.text}
                </div>
              ))}
          </div>
        ))}
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default SurveyDetail;
