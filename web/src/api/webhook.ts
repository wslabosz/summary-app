import { getMessaging, getToken } from "firebase/messaging";

export const triggerSummary = async ({
  videoId,
  model,
  forceSummary,
}: {
  videoId: string;
  model: string;
  forceSummary: boolean;
}) => {
  const messaging = getMessaging();
  const token = await getToken(messaging, {
    vapidKey: import.meta.env.VITE_FIREBASE_VAPID_KEY,
  });
  const baseUrl = `${import.meta.env.VITE_N8N_BASE_URL}webhook-test/summarize`;
  const data = {
    videoId,
    model,
    forceSummary,
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
    return response;
  } catch (e) {
    console.log("Error: ", e);
  }
  return null;
};
