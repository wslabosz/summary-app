import { Box } from "@mui/material";

export const YoutubeEmbed = ({ videoId }: { videoId: string }) => (
  <Box
    alignSelf="center"
    overflow="hidden"
    position="relative"
    width="60%"
    height="24em"
  >
    <iframe
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
      }}
      src={`https://www.youtube.com/embed/${videoId}`}
      allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      title="Embedded youtube"
    />
  </Box>
);
