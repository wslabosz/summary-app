import { createRoot } from "react-dom/client";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import App, { Loader } from "./App";
import "./index.css";
import VideoPage, { VideoPageLoader } from "./pages/Video";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    loader: Loader,
    children: [
      {
        path: "/video",
        element: <VideoPage />,
        loader: VideoPageLoader,
      },
    ],
  },
]);

createRoot(document.getElementById("app")!).render(
  <RouterProvider router={router} />
);
