import { SelectChangeEvent, Stack } from "@mui/material";
import { MessagePayload, getMessaging, onMessage } from "firebase/messaging";
import { useEffect, useState } from "react";
import {
  ActionFunctionArgs,
  ParamParseKey,
  Params,
  useLoaderData,
  useParams,
  useRouteLoaderData,
} from "react-router";
import { SummaryResponse, getSummary } from "../api/summary";
import { SummaryForm } from "../components/SummaryForm";
import { SummaryPanel } from "../components/SummaryPanel";
import { YoutubeEmbed } from "../components/YoutubeIFrame";
import { app } from "../firebase";

type NotificationData = {
  videoId: string;
  model: string;
};

const PathNames = {
  videoPage: "/video/:id",
} as const;

interface URL extends ActionFunctionArgs {
  params: Params<ParamParseKey<typeof PathNames.videoPage>>;
}

const DEFAULT_MODEL = "mistral";

export async function VideoPageLoader({ params }: URL) {
  return getSummary(params.id as string, DEFAULT_MODEL);
}

const VideoPage = () => {
  const params = useParams();
  const messaging = getMessaging(app);
  const initSummary = useLoaderData() as SummaryResponse;
  const [summary, setSummary] = useState<SummaryResponse | undefined>();

  const models = useRouteLoaderData("root") as string[] | undefined;
  // TODO: handle when models is undefined
  const [model, setModel] = useState(models?.[0]);
  const handleChange = (event: SelectChangeEvent) => {
    setModel(event.target.value);
  };

  useEffect(() => {
    setSummary(initSummary);
  }, [params.id]);

  useEffect(() => {
    if (summary) return;

    const handleWindowFocus = async () => {
      const response = await getSummary(params.id as string, model as string);
      setSummary(response);
    };

    window.addEventListener("focus", async () => handleWindowFocus);
    return () =>
      window.removeEventListener("focus", async () => handleWindowFocus);
  }, [model, params.id]);

  onMessage(messaging, async ({ data }: MessagePayload) => {
    console.log("Message received. ", data);
    const { videoId, model } = data as NotificationData;
    const response = await getSummary(videoId, model);
    setSummary(response);
  });

  return (
    <div>
      <h1>Video Page</h1>
      <Stack flex="1" direction="column">
        <YoutubeEmbed videoId={params.id as string} />
        {summary && (
          <SummaryPanel
            videoTitle={summary?.videoTitle}
            summary={summary?.summary}
          />
        )}
        <SummaryForm
          models={models}
          model={model}
          handleSetModel={handleChange}
        />
      </Stack>
    </div>
  );
};

export default VideoPage;
