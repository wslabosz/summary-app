import { Typography } from "@mui/material";
import { useNavigate } from "react-router";

export const AppBar = () => {
  const navigate = useNavigate();

  const handleSubmitEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      const url = (document.getElementById("videoUrlInput") as HTMLInputElement)
        .value;
      if (url) {
        navigate(`/video?url=${url}`);
        // if valid URL, navigate to /video?url={url}
      } else {
        // show error response
        console.log("Invalid URL");
      }
    }
  };

  return (
    <div id="titleBarContainer">
      <div id="titleBar" className="draggable">
        <Typography
          m="auto"
          p="0 1.5em"
          className="draggable"
          variant="inherit"
        >
          Summarize-a-video
        </Typography>
        <input
          id="videoUrlInput"
          className="nonDraggable"
          type="text"
          placeholder="Video URL to summarize"
          onKeyDown={(e) => handleSubmitEnter(e)}
        />
      </div>
    </div>
  );
};
