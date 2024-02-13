import os

from huggingface_hub import InferenceClient
from huggingface_hub.inference._client import ModelStatus

from .config import models


def get_model_status(model_name: str) -> ModelStatus:
    client = InferenceClient(
        token=os.environ.get("HF_API_KEY"),
    )
    return client.get_model_status(model=models[model_name]["id"])
