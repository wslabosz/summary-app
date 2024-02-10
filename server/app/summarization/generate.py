import os
from typing import TypedDict

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
models = {
    "mistral": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "phi": "microsoft/phi-2",
    "orca": "microsoft/Orca-2-13b",
    "olmo": "allenai/OLMo-7B",
    "falcon_sum": "Falconsai/text_summarization",
}

model_id = models["mistral"]
client = InferenceClient(model_id, token=os.environ.get("HF_API_KEY"))


class SummaryResult(TypedDict):
    summary: str
    system_prompt: str


def summarize(text: str) -> SummaryResult:
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
