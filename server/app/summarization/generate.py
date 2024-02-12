import os
from typing import TypedDict

from huggingface_hub import InferenceClient

from .model import models


class SummaryResult(TypedDict):
    summary: str
    system_prompt: str


# TODO: WORK ON THE SUMMARY MODULE
def summarize(text: str, model: str | None) -> SummaryResult:
    if model is None:
        model = "mistral"
    model_id = models[model]
    client = InferenceClient(model_id, token=os.environ.get("HF_API_KEY"))

    system_prompt = """
    ### Instruction ###
    Summarize the video material transcription delimited by triple backquotes.
    """

    if model_id == models["mistral"]:
        input_prompt = f"<s>[INST] {system_prompt} \n\n "

    input_prompt = input_prompt + f"```{text}```" + " [/INST] "
    generate_kwargs = dict(
        temperature=0.1,
        max_new_tokens=512,
        top_p=0.95,
        best_of=1,
        repetition_penalty=1.2,
        do_sample=True,
        seed=11,
    )

    response = client.text_generation(input_prompt, **generate_kwargs, details=True)

    print(response.details.finish_reason)
    return {"summary": response.generated_text, "system_prompt": system_prompt}
