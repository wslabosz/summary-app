models = {
    "mistral": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "phi": "microsoft/phi-2",
    "orca": "microsoft/Orca-2-13b",
    "olmo": "allenai/OLMo-7B",
    "falcon_sum": "Falconsai/text_summarization",
}


def get_model_list():
    return models.keys()
