import os

from huggingface_hub import InferenceClient

from .config import models


class InferenceModel:
    """
    This class represents an Inference Client with its configuration.
    """

    def __init__(self, model_name: str, config_overrides: dict = None):
        """
        Initializes the InferenceModel object.

        Args:
            model_name (str): The name of the LLM model from the Hugging Face Hub.
            config_overrides (dict, optional): A dictionary of options to override the default model configuration. Defaults to None.
        """
        self.model_name = model_name
        model = models[model_name]
        self.client = InferenceClient(
            model=model["id"],
            token=os.environ.get("HF_API_KEY"),
            timeout=20,
        )
        self.type = model["type"]
        if self.type == "text-generation":
            self.system_prompt = model["system_prompt"]
            self.prompt_template = model["prompt_template"]

        self.config = model["config"]
        self.options = {
            "use_cache": True,
            "wait_for_model": True,
        }
        if config_overrides:
            for key, value in config_overrides.items():
                setattr(self.config, key, value)

    def generate(self, input_prompt: str) -> tuple[dict, str]:
        """
        Args:
        Returns:
        """
        if self.type == "text-summarization":
            return (
                self.client.summarization(
                    input_prompt,
                    parameters=self.config,
                ),
                "text-summarization",
            )
        return (
            self.client.text_generation(
                self.prompt_template(self.system_prompt, input_prompt),
                **self.config,
            ),
            self.prompt_template(self.system_prompt, "<transcription>"),
        )
