import React from "react";
import styled from "styled-components";
import "./homeScreen.css";
import { useState } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";
import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import { QuestionTile } from "../components/Home/questionTile";
import { RecommendationTile } from "../components/Home/recommendationTile";
import { CircularProgress } from "@mui/material";
import { Navbar } from "../components/common/navbar";

export function HomeScreen() {
  const location = useLocation();
  const userPref = location.state;
  const [askedQuery, setAskedQuery] = useState(null);
  let [response, setResponses] = useState([]);
  let [fetchingResponse, setFetchingResponse] = useState(false);

  async function handleSubmit(event) {
    //console.log(event);
    event.preventDefault();

    setFetchingResponse(true);

    let res = await axios.get(`http://localhost:8000/items/${askedQuery}`, {
      params: {
        age: 20,
        location: "mumbai",
        gender: "male",
        user_instructions: "jo me bolu bas wahi recommend karna",
        curr_date: "23 august",
      },
    });
    console.log(res.data);
    // eslint-disable-next-line
    setResponses((prevResponses) => {
      //console.log([...prevRecommendations, null]);
      setFetchingResponse(false);
      return [...prevResponses, { askedQuery: askedQuery, response: res.data }];
    });
  }
  return (
    <div>
      <Navbar />
      <div className="title-text">
        {!askedQuery
          ? "Welcome back"
          : "Hope you liked our recommended outfit!"}
      </div>
      <div>
        {response.map((queryResult, idx) => {
          console.log(queryResult);
          if ("recommendations" in queryResult.response) {
            return (
              <RecommendationTile
                recommendationsList={queryResult.response.recommendations}
              />
            );
          } else
            return <QuestionTile question={queryResult.response.question} />;
        })}
      </div>
      {fetchingResponse === true ? <CircularProgress /> : null}
      <div className="p-6 flex justify-center">
        <div className="chatbar-wrapper">
          <form onSubmit={handleSubmit}>
            <IconButton type="submit" aria-label="search">
              <SearchIcon
                style={{ fill: "black", fontSize: "1.5rem", margin: "0px" }}
              />
            </IconButton>
            <input
              type="text"
              className="text-field"
              autoFocus
              value={askedQuery}
              onInput={(e) => setAskedQuery(e.target.value)}
            />
          </form>
        </div>
      </div>
    </div>
  );
}
