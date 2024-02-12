import axios, { AxiosResponse } from "axios";

export type ModelResponse = {
  models: string[];
};

export async function getModels(
  baseURL: string = import.meta.env.VITE_API_BASE_URL
): Promise<ModelResponse | undefined> {
  try {
    const response: AxiosResponse<ModelResponse> = await axios.get(
      `${baseURL}models`,
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
