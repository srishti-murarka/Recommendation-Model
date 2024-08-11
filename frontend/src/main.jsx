import "regenerator-runtime/runtime";
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import Onboarding from "./pages/Onboarding";
// import App from "./App.jsx";
import "./index.css";
import { Outlet, RouterProvider, createBrowserRouter } from "react-router-dom";
import Chat from "./pages/Chat/Chat";

const router = createBrowserRouter([
  {
    element: (
      <>
        <Outlet />
      </>
    ),
    children: [
      {
        path: "/",
        element: <App />,
      },
    ],
  },
  {
    element: (
      <>
        <Outlet />
      </>
    ),
    children: [
      {
        path: "/onboarding",
        element: <Onboarding />,
      },
    ],
  },
  {
    element: (
      <>
        <Outlet />
      </>
    ),
    children: [
      {
        path: "/test",
        element: <Chat />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
