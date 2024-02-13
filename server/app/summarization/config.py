models = {
    "mistral": {
        "id": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "type": "text-generation",
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
    # not loaded
    "phi": {
        "id": "microsoft/phi-2",
        "type": "text-generation",
        "system_prompt": """You are an expert summary maker. Summarize input video material transcription.""",
        "prompt_template": lambda instruction, input: f"""Instruction: {instruction}\nInput: "{input}"\nOutput: """,
        "config": {
            "temperature": 0.01,
            "max_new_tokens": 250,
            "top_p": 0.95,
            "repetition_penalty": 1.2,
            "do_sample": True,
        },
    },
    "llama": {
        # 7b also works
        "id": "meta-llama/Llama-2-13b-hf",
        "type": "text-generation",
        "system_prompt": """### Instruction ### You are an expert summary maker. Summarize input video material transcription.""",
        "prompt_template": lambda instruction, input: f"""<s>[INST] {instruction}\nInput: "{input}"\n [/INST]""",
        "config": {
            "temperature": 0.01,
            "max_new_tokens": 512,
            "top_p": 0.95,
            # "top_k": 50,
            "best_of": 1,
            "repetition_penalty": 1.2,
            "do_sample": True,
            "seed": 11,
            # "max_time": 120,
        },
    },
    "falcon": {
        "id": "Falconsai/text_summarization",
        "type": "text-summarization",
        "config": {
            "temperature": 0.01,
            "top_p": 0.95,
            "repetition_penalty": 1.2,
            # "top_k": 50,
            # "min_length": 250,
            # "max_length": 200,
            # "max_time": 120,
        },
    },
    # TOO BIG
    # "orca": {
    #     "id": "microsoft/Orca-2-13b",
    # },
    # "olmo": {
    #     "id": "allenai/OLMo-7B",
    # },
}


def get_model_list():
    return models.keys()
