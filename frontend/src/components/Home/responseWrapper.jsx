import "./responseWrapper.css";
import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import axios from "axios";
import { QuestionTile } from "./questionTile";
import { RecommendationTile } from "./recommendationTile";
import { useState } from "react";
import { CircularProgress } from "@mui/material";

export function ResponseWrapper() {
  let [respones, setResponses] = useState([]);
  let [askedQuery, setAskedQuery] = useState("");
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
    setResponses((prevResponses) => {
      //console.log([...prevRecommendations, null]);
      setFetchingResponse(false);
      return [...prevResponses, { askedQuery: askedQuery, response: res.data }];
    });
  }

  return (
    <div>
      <div className="title-text">
        {!askedQuery
          ? "ShopAI will help you plan an outfit"
          : "Hope you liked our recommended outfit!"}
      </div>
      <div>
        {respones.map((queryResult, idx) => {
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
