from typing import TypedDict

from .InferenceModel import InferenceModel


class SummaryResult(TypedDict):
    summary: str
    system_prompt: str


# TODO: WORK ON THE SUMMARY MODULE
def summarize(text: str, model: str | None) -> SummaryResult:
    print(f"Summarizing with model: {model}")
    client = InferenceModel(model_name=model)
    response, system_prompt = client.generate(text)
    print("Summary generated")
    return {"summary": response, "system_prompt": system_prompt}
