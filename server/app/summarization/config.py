models = {
    "mistral": {
        "id": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "system_prompt": """### Instruction ### You are an expert summary maker. Summarize input video material transcription.""",
        "prompt_template": lambda instruction, input: f"""<s>[INST] {instruction}\nInput: "{input}"\n [/INST]""",
        "config": {
            "temperature": 0.01,
            "max_new_tokens": 512,
            "top_p": 0.95,
            "best_of": 1,
            "repetition_penalty": 1.2,
            "do_sample": True,
            "seed": 11,
        },
    },
    "phi": {
        "id": "microsoft/phi-2",
        "system_prompt": """### Instruction ### You are an expert summary maker. Summarize input video material transcription.""",
        "prompt_template": lambda instruction, input: f"""Instruction: {instruction}\nInput: "{input}"\nOutput: """,
        "config": {
            "temperature": 0.01,
            "max_new_tokens": 250,
            "top_p": 0.95,
            "repetition_penalty": 10,
            "do_sample": True,
        },
    },
    "orca": "microsoft/Orca-2-13b",
    "olmo": "allenai/OLMo-7B",
    "falcon": "Falconsai/text_summarization",
}


def get_model_list():
    return models.keys()
