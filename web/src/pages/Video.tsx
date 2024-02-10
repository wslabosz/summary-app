import { useLoaderData } from "react-router-dom";

export async function VideoPageLoader({
  request: { url },
}: {
  request: { url: string };
}) {
  const videoId = new URL(url).searchParams.get("url");
  const baseUrl = `${import.meta.env.VITE_N8N_BASE_URL}webhook-test/summarize`;

  const data = {
    videoId,
  };

  try {
    const response = await fetch(baseUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
      mode: "no-cors",
    });
    return videoId;
  } catch (e) {
    console.log("Error: ", e);
  }
  return null;
}

const VideoPage = () => {
  const data = useLoaderData() as string;
  console.log(data);
  return (
    <div>
      <h1>{data}</h1>
    </div>
  );
};

export default VideoPage;
