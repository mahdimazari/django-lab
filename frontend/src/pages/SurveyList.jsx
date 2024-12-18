import React, { useEffect, useState } from "react";
import api from "../api";
import "../styles/SurveyWizard.css";
import { ACCESS_TOKEN } from "../constants";

const SurveyList = () => {
  const [surveys, setSurveys] = useState([]);
  const [responses, setResponses] = useState([]);

  useEffect(() => {
    // api.get("/api/surveys/").then((response) => {
    //   setSurveys(response.data);
    // });
    api.get("/api/surveys/accessible/").then((response) => {
      setSurveys(response.data);
    });

    api
      .get("/api/survey-responses/", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`,
        },
      })
      .then((response) => {
        console.log("repsonse", response);
        setResponses(response.data);
      });
  }, []);

  return (
    // <div>
    //   <h1>Surveys</h1>
    //   <ul>
    //     {surveys ? (
    //       surveys.map(
    //         (survey) => (
    //           console.log("serv", survey),
    //           (
    //             <li key={survey.id}>
    //               <a href={`survey/${survey.id}`}>{survey.title}</a>
    //             </li>
    //           )
    //         )
    //       )
    //     ) : (
    //       <></>
    //     )}
    //   </ul>
    // </div>
    <>
      <div className="surveys-container">
        <h1 className="surveys-title">Surveys Disponibles</h1>
        {surveys.length > 0 ? (
          <div className="surveys-grid">
            {surveys.map((survey) => (
              <div className="survey-card" key={survey.id}>
                <h3 className="survey-title">{survey.title}</h3>
                <p className="survey-description">{survey.description}</p>
                <a href={`survey/${survey.id}`} className="survey-button">
                  Répondre au Survey
                </a>
              </div>
            ))}
          </div>
        ) : (
          <p className="no-surveys">Aucun survey disponible pour vous.</p>
        )}
      </div>
      <div className="responses-container">
        <h1 className="responses-title">Mes Réponses</h1>
        {responses.length > 0 ? (
          <ul className="responses-list">
            {responses.map((response) => (
              <li className="response-item" key={response.id}>
                <p>
                  <strong>Survey Name:</strong>{" "}
                  <a
                    href={`survey-responses/${response.id}`}
                    className="survey-link"
                  >
                    {response.survey.title}
                  </a>
                </p>
                <p>
                  <strong>Date de Réponse:</strong>{" "}
                  {new Date(response.created_at).toLocaleString("fr-FR", {
                    day: "2-digit",
                    month: "long",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </p>
                <p>
                  <strong>Créé par:</strong> {response.created_by.username}
                </p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="no-responses">
            Vous n`avez encore soumis aucune réponse.
          </p>
        )}
      </div>
    </>
  );
};

export default SurveyList;
