import React, { useEffect } from "react";
import styled from "styled-components";
import axios from "axios";
import { MdPerson } from "react-icons/md";
import { GoHubot } from "react-icons/go";
import {
  PiPaperPlaneRightFill,
  PiShuffle,
  PiLink,
  PiMicrophone,
} from "react-icons/pi";
import { CircularProgress, Tooltip, IconButton } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import { createSpeechlySpeechRecognition } from "@speechly/speech-recognition-polyfill";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

const appId = "d2a075a3-0121-4ff5-86a0-6dfdb5f28ed8";
const SpeechlySpeechRecognition = createSpeechlySpeechRecognition(appId);
SpeechRecognition.applyPolyfill(SpeechlySpeechRecognition);

type ChatBotProps = {
  queryAsked: string;
  userPref: {
    age: number;
    gender: string;
    extra: string;
  };
  cartItems: any[];
  setCartItems: React.Dispatch<React.SetStateAction<any[]>>;
  setQueryAsked: React.Dispatch<React.SetStateAction<string>>;
};

export default function ChatBot<ChatBotProps>({
  queryAsked,
  userPref,
  cartItems = [],
  setCartItems,
  setQueryAsked,
}) {
  const [inputValue, setInputValue] = React.useState("");

  const chatInputRef = React.useRef<HTMLInputElement>(null);

  // Local query asked in ChatBot Page
  const [localQueryAsked, setLocalQueryAsked] = React.useState();

  // Tracking First API call
  const [isFirstCall, setIsFirstCall] = React.useState(true);

  // Storing the list of the conversation
  const [response, setResponse] = React.useState<
    Array<{ role: string; response: any }>
  >([{ role: "user", response: queryAsked }]);
  console.log(queryAsked);
  console.log(userPref);

  // Date in the format of "23 august"
  const monthNames = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
  ];

  // Get the current date
  const currentDate = new Date();

  // Extract day and month
  const day = currentDate.getDate();
  const month = monthNames[currentDate.getMonth()];

  // Form the desired format
  const dateMonth = `${day} ${month}`;

  useEffect(() => {
    // Remove history before running the query
    axios.get("http://localhost:8000/clear").then((res) => {
      // First Query Call
      axios
        .get(`http://localhost:8000/items/${queryAsked}`, {
          params: {
            age: userPref.age,
            location: userPref.state,
            gender: userPref.gender.toLowerCase(),
            user_instructions: userPref.extra,
            curr_date: dateMonth,
          },
        })
        .then((res) => {
          if (res.data) {
            setResponse((prevResponses) => {
              setIsFirstCall(false);
              return [...prevResponses, { role: "bot", response: res.data }];
            });
          }
        });
    });
  }, []);

  // useEffect(() => {
  //   if (localQueryAsked) {
  //     axios
  //       .get(`http://localhost:8000/items/${localQueryAsked}`, {
  //         params: {
  //           age: userPref.age,
  //           location: userPref.state,
  //           gender: userPref.gender.toLowerCase(),
  //           user_instructions: userPref.extra,
  //           curr_date: dateMonth,
  //         },
  //       })
  //       .then((res) => {
  //         if (res.data) {
  //           setResponse((prevResponses) => {
  //             setIsFirstCall(false);
  //             return [...prevResponses, { role: "bot", response: res.data }];
  //           });
  //         }
  //       });
  //   }
  // }, [localQueryAsked]);

  console.log(response);

  // Speech Recognition
  const { transcript, browserSupportsSpeechRecognition } =
    useSpeechRecognition();
  const startListening = async () => {
    SpeechRecognition.startListening({ continuous: true, language: "en-IN" });
    setInputValue(transcript);
  };

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  if (isFirstCall)
    return (
      <div
        style={{
          color: "#fff",
          padding: "6rem",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <CircularProgress />
      </div>
    );

  return (
    <ChatBotWrapper>
      <ChatList>
        {response?.map((res) =>
          res.role === "user" ? (
            <UserMessage message={res.response} />
          ) : (
            <BotMessage
              message={res.response}
              setResponse={setResponse}
              setCartItems={setCartItems}
            />
          )
        )}
      </ChatList>
      <form
        className="input"
        onSubmit={(e) => {
          e.preventDefault();
          const formData = new FormData(e.currentTarget);
          const data = Object.fromEntries(formData.entries());
          setResponse((prevResponses) => [
            ...prevResponses,
            { role: "user", response: data.query },
          ]);
          setLocalQueryAsked(data.query as string);
          chatInputRef.current!.value = "";
          if (data.query) {
            axios
              .get(`http://localhost:8000/items/${data.query}`, {
                params: {
                  age: userPref.age,
                  location: userPref.state,
                  gender: userPref.gender.toLowerCase(),
                  user_instructions: userPref.extra,
                  curr_date: dateMonth,
                },
              })
              .then((res) => {
                if (res.data) {
                  setResponse((prevResponses) => {
                    setIsFirstCall(false);
                    return [
                      ...prevResponses,
                      { role: "bot", response: res.data },
                    ];
                  });
                }
              });
            setInputValue("");
          }
        }}
      >
        <Tooltip title="Clear History">
          <IconButton
            onClick={() => {
              axios.get("http://localhost:8000/clear");
              setQueryAsked(null);
            }}
          >
            <DeleteIcon />
          </IconButton>
        </Tooltip>
        <input
          ref={chatInputRef}
          type="text"
          name="query"
          id="query"
          placeholder="What Outfit are you looking for today?"
          // onChange={(e) => setInputValue(e.target.value)}
          // value={inputValue}
          autoFocus={true}
          required
        />
        <button
          onTouchStart={startListening}
          onMouseDown={startListening}
          onTouchEnd={SpeechRecognition.stopListening}
          onMouseUp={SpeechRecognition.stopListening}
        >
          <PiMicrophone />
        </button>
        <button type="submit">
          <PiPaperPlaneRightFill />
        </button>
      </form>
    </ChatBotWrapper>
  );
}

type UserMessageProps = {
  message: string;
};

function UserMessage<UserMessageProps>({ message }) {
  return (
    <div
      style={{
        width: "100%",
        display: "flex",
        justifyContent: "flex-end",
        flexWrap: "wrap",
      }}
    >
      <div style={{ display: "flex", alignItems: "flex-end", gap: "4px" }}>
        <div className="message-wrapper">
          <p>{message}</p>
        </div>
        <div
          style={{
            width: "24px",
            height: "24px",
            borderRadius: "50%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            background: "#5F5CD5",
          }}
        >
          <MdPerson color="white" />
        </div>
      </div>
    </div>
  );
}

type BotMessageProps = {
  setResponse: React.Dispatch<
    React.SetStateAction<
      {
        role: string;
        response: string;
      }[]
    >
  >;
  setCartItems: React.Dispatch<
    React.SetStateAction<
      {
        search_query: string;
        product_link: string;
        product_name: string;
        product_price: string;
        image_link: string;
      }[]
    >
  >;
} & UserMessageProps;

function BotMessage<BotMessageProps>({ message, setResponse, setCartItems }) {
  if (message && message.question) {
    return (
      <div
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "flex-start",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "flex-end",
            gap: "4px",
          }}
        >
          <div
            style={{
              minWidth: "24px",
              minHeight: "24px",
              width: "24px",
              height: "24px",
              borderRadius: "50%",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              background: "#fff",
            }}
          >
            <GoHubot />
          </div>
          <div className="message-wrapper">
            <p>{message.question}</p>
          </div>
        </div>
      </div>
    );
  } else if (message && message.recommendations) {
    return (
      <div
        style={{
          width: "100%",
          display: "flex",
          flexWrap: "wrap",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "flex-end",
            gap: "4px",
          }}
        >
          <div
            style={{
              width: "24px",
              height: "24px",
              borderRadius: "50%",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              background: "#fff",
            }}
          >
            <GoHubot />
          </div>
          <div className="recommendations-wrapper">
            {message.recommendations.map((rec) => (
              <div>
                <div
                  style={{
                    background: `url(${rec.image_link}) no-repeat center center`,
                    backgroundSize: "cover",
                    width: "120px",
                    height: "120px",
                    borderRadius: "6px 6px 0 0",
                  }}
                >
                  <div
                    style={{ display: "flex", flexDirection: "row-reverse" }}
                  >
                    <button
                      style={{
                        backgroundColor: "#C86C53",
                        padding: "4px",
                        borderRadius: "6px",
                      }}
                      onClick={() => window.open(rec.product_link, "_blank")}
                    >
                      <PiLink color="white" />
                    </button>
                  </div>
                  {/* <p>{rec.product_link}</p> */}
                </div>
                <div style={{ display: "flex" }}>
                  <div
                    style={{
                      flex: 1,
                      background: "#5F5CD5",
                      display: "flex",
                      justifyContent: "center",
                      alignItems: "center",
                      borderRadius: "0 0 0 6px",
                      color: "#fff",
                      padding: "4px",
                    }}
                  >
                    <p>{rec.product_price}</p>
                  </div>
                  <button
                    style={{
                      backgroundColor: "#C86C53",
                      display: "flex",
                      justifyContent: "center",
                      alignItems: "center",
                      padding: "4px",
                    }}
                    onClick={(e) => {
                      e.preventDefault();
                      axios
                        .get(`http://localhost:8000/regenerate-item`, {
                          params: {
                            search_query: rec.search_query,
                            product_name: rec.product_name,
                          },
                        })
                        .then((res) => {
                          if (res.data) {
                            setResponse((prevResponses) => {
                              return [
                                ...prevResponses,
                                { role: "bot", response: res.data },
                              ];
                            });
                          }
                        });
                    }}
                  >
                    <PiShuffle color="white" />
                  </button>
                  <button
                    style={{
                      background: "#fff",
                      display: "flex",
                      justifyContent: "center",
                      alignItems: "center",
                      padding: "4px",
                      borderRadius: "0 0 6px 0",
                    }}
                    onClick={() => {
                      axios.get(`http://localhost:8000/cart-history/${rec.product_name}`)
                      setCartItems((prevCartItems) => {
                        return [...prevCartItems, rec];
                      });
                    }}
                  >
                    <ShoppingCartIcon />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }
  return null;
}

const ChatBotWrapper = styled.div`
  min-height: 100vh;
  min-width: 100vw;
  padding: 6rem;
  display: flex;
  justify-content: center;
  .input {
    width: calc(100% / 2);
    bottom: 1rem;
    background: #d9d9d9;
    border-radius: 20px;
    padding: 6px 8px 6px 6px;
    display: flex;
    align-items: center;
    position: fixed;
    gap: 0.5rem;
    input {
      all: unset;
      padding: 0.5rem;
      flex-grow: 1;
    }
    button {
      display: flex;
      gap: 4px;
      border-radius: 16px;
      background: #c86c53;
      color: #fff;
      padding: 12px 12px;
      font-weight: 400;
    }
  }
`;

const ChatList = styled.div`
  width: calc(100% / 2);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;

  .message-wrapper {
    padding: 1rem;
    background-color: #d9d9d9;
    border-radius: 8px;
    p {
      color: #000;
      font-weight: 400;
      flex-wrap: wrap;
    }
  }
  .recommendations-wrapper {
    padding: 1rem;
    background-color: #d9d9d9;
    border-radius: 8px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    flex-wrap: wrap;
    width: ;
    gap: 1rem;
  }
`;
