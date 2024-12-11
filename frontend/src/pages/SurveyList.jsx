import React, { useEffect, useState } from "react";
// import axios from "axios";
import api from "../api";

const SurveyList = () => {
  const [surveys, setSurveys] = useState([]);

  useEffect(() => {
    api.get("/api/surveys/").then((response) => {
      setSurveys(response.data);
    });
  }, []);

  return (
    <div>
      <h1>Surveys</h1>
      <ul>
        {surveys ? (
          surveys.map(
            (survey) => (
              console.log("serv", survey),
              (
                <li key={survey.id}>
                  <a href={`survey/${survey.id}`}>{survey.title}</a>
                </li>
              )
            )
          )
        ) : (
          <></>
        )}
      </ul>
    </div>
  );
};

export default SurveyList;
