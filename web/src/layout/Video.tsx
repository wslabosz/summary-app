import { Outlet } from "react-router";

const VideoLayout = () => {
  return (
    <div>
      <h1>Videos</h1>
      <Outlet />
    </div>
  );
};

export default VideoLayout;
