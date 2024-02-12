import { createRoot } from "react-dom/client";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import App, { Loader } from "./App";
import "./index.css";
import VideoLayout from "./layout/Video";
import VideoPage, { VideoPageLoader } from "./pages/Video";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    loader: Loader,
    id: "root",
    shouldRevalidate: () => false,
    children: [
      {
        path: "/video",
        element: <VideoLayout />,
        children: [
          {
            path: ":id",
            element: <VideoPage />,
            loader: VideoPageLoader,
          },
        ],
      },
    ],
  },
]);

createRoot(document.getElementById("app")!).render(
  <RouterProvider router={router} />
);
