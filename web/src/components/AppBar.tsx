import HomeIcon from "@mui/icons-material/Home";
import { IconButton, Typography } from "@mui/material";
import { useNavigate } from "react-router";

export const AppBar = () => {
  const navigate = useNavigate();
  const handleHomeClick = () => {
    navigate(`/`);
  };

  const handleSubmitEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      const url = (document.getElementById("videoUrlInput") as HTMLInputElement)
        .value;
      if (url) {
        // TODO: check if valid yt url
        const videoId = url.split("watch?v=")[1];
        navigate(`/video/${videoId}`);
      } else {
        // TODO: show error response
        console.log("Invalid URL");
      }
    }
  };

  return (
    <div id="titleBarContainer">
      <div id="titleBar" className="draggable">
        <IconButton
          sx={{ pl: "0.5em" }}
          aria-label="redirect home"
          onClick={handleHomeClick}
        >
          <HomeIcon />
        </IconButton>
        <Typography
          m="auto"
          p="0 0.5em"
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
          onKeyDown={handleSubmitEnter}
        />
      </div>
    </div>
  );
};
