import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
} from "@mui/material";
import {
  MessagePayload,
  getMessaging,
  getToken,
  onMessage,
} from "firebase/messaging";
import { useEffect, useState } from "react";
import {
  ActionFunctionArgs,
  ParamParseKey,
  Params,
  useParams,
} from "react-router";
import { SummaryResponse, getSummary } from "../api/summary";
import { SummaryPanel } from "../components/SummaryPanel";
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

export async function VideoPageLoader({ params }: URL) {
  const messaging = getMessaging(app);
  const videoId = params.id;
  const baseUrl = `${import.meta.env.VITE_N8N_BASE_URL}webhook/summarize`;
  const token = await getToken(messaging, {
    vapidKey: import.meta.env.VITE_FIREBASE_VAPID_KEY,
  });

  if (!videoId) {
    // TODO: show error response
    return null;
  }

  const data = {
    videoId,
    model: "mistral",
    // TODO: handle this
    // forceSummary: true,
  };

  try {
    const response = await fetch(baseUrl, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "client-token": token,
      },
      body: JSON.stringify(data),
    });
    return videoId;
  } catch (e) {
    console.log("Error: ", e);
  }
  return null;
}

const VideoPage = () => {
  const params = useParams();
  const messaging = getMessaging();
  const [model, setModel] = useState("mistral");
  const [summary, setSummary] = useState<SummaryResponse | undefined>();
  const handleChange = (event: SelectChangeEvent) => {
    setModel(event.target.value);
  };
  const models = ["mistral", "phi", "orca", "olmo", "falcon_sum"];

  useEffect(() => {
    const handleWindowFocus = async () => {
      if (summary) return;
      const response = await getSummary(params.id as string, model);
      setSummary(response);
    };
    window.addEventListener("focus", async () => handleWindowFocus());

    return () => {
      window.removeEventListener("focus", async () => handleWindowFocus());
    };
  }, []);

  onMessage(messaging, async ({ data }: MessagePayload) => {
    console.log("Message received. ", data);
    const { videoId, model } = data as NotificationData;
    const response = await getSummary(videoId, model);
    setSummary(response);
  });

  useEffect(() => {
    setSummary(undefined);
  }, [params.id]);

  return (
    <div>
      <FormControl fullWidth>
        <InputLabel id="select-model-label">Model</InputLabel>
        <Select
          labelId="select-model-label"
          id="select-model"
          label="model"
          value={model}
          onChange={handleChange}
        >
          {models.map((model) => (
            <MenuItem key={model} value={model}>
              {model}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      {summary && (
        <SummaryPanel
          videoTitle={summary?.videoTitle}
          summary={summary?.summary}
        />
      )}
    </div>
  );
};

export default VideoPage;
