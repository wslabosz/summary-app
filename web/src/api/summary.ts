import axios, { AxiosResponse } from "axios";

export type SummaryResponse = {
  videoId: string;
  videoTitle: string;
  dateCreated: string;
  summary: string;
  model: string;
};

export async function getSummary(
  videoId: string,
  model?: string,
  baseURL: string = import.meta.env.VITE_API_BASE_URL
): Promise<SummaryResponse | undefined> {
  try {
    const response: AxiosResponse<SummaryResponse> = await axios.get(
      `${baseURL}summary/${videoId}/${model ?? "mistral"}`,
      {
        headers: {
          "content-type": "application/json",
        },
      }
    );

    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error(`API error: ${response.statusText}`);
    }
  } catch (error) {
    console.error("Error fetching summary:", error);
    return;
  }
}
