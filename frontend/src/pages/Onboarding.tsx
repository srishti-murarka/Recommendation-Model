import React from "react";
import styled from "styled-components";
import { Navbar } from "../components/common/navbar";
import { useNavigate } from "react-router-dom";

export default function Onboarding() {
  const navigate = useNavigate();
  const [userState, setUserState] = React.useState("");

  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
      function (position) {
        var latitude = position.coords.latitude;
        var longitude = position.coords.longitude;

        var apiUrl = `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`;

        fetch(apiUrl)
          .then((response) => response.json())
          .then((data) => {
            if (data && data.address) {

              // var address = data.address;
              // var formattedAddress = `${address.road || ""}, ${
              //   address.city || ""
              // }, ${address.state || ""}, ${address.country || ""}`;
              setUserState(data.address.state)
              console.log("User's Address:", data.address.state);
            } else {
              console.log("Address not found.");
            }
          })
          .catch((error) => {
            console.error("Error fetching address:", error);
          });
      },
      function (error) {
        setUserState("Guwahati")
        console.error("Error Code = " + error.code + " - " + error.message);
      }
    );
  } else {
    console.log("Geolocation is not available in this browser.");
  }

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(formData.entries());
    data["state"] = userState;
    navigate("/test", {
      state: data,
    });
  };

  return (
    <PageWrapper>
      <Navbar CartDisabled={true} />
      <ContainerWrapper>
        <Container>
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: "16px",
              color: "#fff",
            }}
          >
            <h1 style={{ fontSize: "2rem", fontWeight: 500 }}>
              Welcome to ShopAI
            </h1>
            <p style={{ textAlign: "center" }}>
              Press fill the below details
              <br />
              before proceeding ahead
            </p>
          </div>
          <form
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "1.5rem",
              color: "#fff",
            }}
            onSubmit={onSubmit}
          >
            <div
              style={{ display: "flex", flexDirection: "column", gap: "6px" }}
            >
              <label htmlFor="gender" style={{ fontSize: "20px" }}>
                Gender*
              </label>
              <Input type="text" name="gender" id="gender" required />
            </div>
            <div
              style={{ display: "flex", flexDirection: "column", gap: "6px" }}
            >
              <label htmlFor="age" style={{ fontSize: "20px" }}>
                Age*
              </label>
              <Input type="number" name="age" id="age" required />
            </div>
            <div
              style={{ display: "flex", flexDirection: "column", gap: "6px" }}
            >
              <label htmlFor="extra" style={{ fontSize: "20px" }}>
                Any Specific Instructions
              </label>
              <textarea
                name="extra"
                id="extra"
                style={{
                  minHeight: "6rem",
                  width: "100%",
                  padding: "1rem",
                  borderRadius: "8px",
                  color: "#000",
                  backgroundColor: "#f8f8f8",
                }}
              />
            </div>
            <div style={{ display: "flex", justifyContent: "center" }}>
              <button
                type="submit"
                style={{
                  padding: "1rem",
                  borderRadius: "8px",
                  backgroundColor: "#C86C53",
                  color: "#fff",
                  fontSize: "1.25rem",
                }}
              >
                Submit
              </button>
            </div>{" "}
          </form>
          <p style={{ color: "#fff" }}>
            Note: Please allow the location access after clicking submit!
          </p>
        </Container>
      </ContainerWrapper>
    </PageWrapper>
  );
}

const PageWrapper = styled.div`
  width: 100vw;
  height: 100vh;
  background-color: #171717;
`;

const ContainerWrapper = styled.div`
  padding-top: 4rem;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const Container = styled.div`
  width: calc(100vw / 3);
  background-color: #1e1e1e;
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const Input = styled.input`
  width: 100%;
  padding: 1rem;
  border-radius: 8px;
  color: #000;
  background-color: #f8f8f8;
`;
