from typing import TypedDict

from app.summarization.status import get_model_status

from .InferenceModel import InferenceModel


class SummaryResult(TypedDict):
    summary: str
    system_prompt: str


# TODO: WORK ON THE SUMMARY MODULE
def summarize(text: str, model: str) -> SummaryResult:
    model_status = get_model_status(model)
    print(model_status)
    if model_status.state == "TooBig":
        return {"summary": "Model too big to load", "system_prompt": ""}
    client = InferenceModel(model_name=model)
    try:
        response, system_prompt = client.generate(text)
    except Exception as e:
        print(f"Error: {e}")
        return {"summary": "An error occurred", "system_prompt": ""}
    return {"summary": response, "system_prompt": system_prompt}
