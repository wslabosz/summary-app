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
        self.client = InferenceClient(
            models[model_name]["id"], token=os.environ.get("HF_API_KEY")
        )

        self.system_prompt = models[model_name]["system_prompt"]
        self.prompt_template = models[model_name]["prompt_template"]
        self.config = models[model_name]["config"]
        if config_overrides:
            for key, value in config_overrides.items():
                setattr(self.config, key, value)

    def generate(self, input_prompt: str) -> tuple[dict, str]:
        """
        Args:
        Returns:
        """
        if self.model_name == "falcon":
            return (
                self.client.text_generation(
                    self.prompt_template(self.system_prompt, input_prompt),
                    **self.config,
                ),
                self.prompt_template(self.systemprompt, "<transcription>"),
            )
        return (
            self.client.text_generation(
                self.prompt_template(self.system_prompt, input_prompt),
                **self.config,
            ),
            self.prompt_template(self.system_prompt, "<transcription>"),
        )
