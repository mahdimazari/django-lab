import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";
import "../styles/SurveyResponseDetails.css";

const SurveyResponseDetail = () => {
  const { id } = useParams();

  const [responseData, setResponseData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(`/api/survey-responses/${id}/`).then((response) => {
      console.log("response dfetial", response);
      setResponseData(response.data);
      setLoading(false);
    });
  }, [id]);

  if (loading) return <p>Loading...</p>;

  return (
    <div className="survey-response-container">
      <h1 className="survey-response-title">Survey Response</h1>
      <p className="survey-title">
        <strong>Survey Title:</strong> {responseData.survey.title}
      </p>

      <div className="survey-answers">
        {responseData.answers.map((answer, index) => (
          <div className="survey-answer" key={index}>
            <p className="question-text">{answer.question_text}</p>
            <p className="answer-text">
              {answer.text || answer.choice_text || ""}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SurveyResponseDetail;
