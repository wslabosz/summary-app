import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tokens import num_tokens_from_messages

# load environment variables from .env
load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "summarize_video",
            "description": "Summarize the video material transcription and determine the tags for the video material.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "The summary of the video material transcription.",
                    },
                    "tags": {
                        "type": "array",
                        "description": "Tags used to categorize the video material content.",
                        "items": {"type": "string"},
                    },
                },
                "required": ["summary", "tags"],
            },
        },
    },
]


def complete_chat(transcription_path: str, model: str = "gpt-3.5-turbo-1106"):
    with open(transcription_path) as f:
        transcript = f.readlines()

        messages = [
            {
                "role": "system",
                "content": """Write a concise summary of the video material transcription delimited by triple backquotes.
                                Return back a valid json object with the following structure:
                                {
                                    "summary": "The summary of the video material transcription",
                                    "tags": "[array of tags to help categorize the video material]",
                                }""",
            },
            {
                "role": "user",
                "content": f"```{''.join(transcript)}```",
            },
        ]

    tokens = num_tokens_from_messages(messages, model=model)
    print(f"Number of tokens: {tokens}")

    # actually we can base on the newline characters in the input file
    if len(transcript) < 2:
        print("Using stuffing method to summarize document")
        response = client.chat.completions.create(
            messages=messages,
            model=model,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "summarize_video"}},
            response_format={"type": "json_object"},
        )
    else:
        print("Using refine method to summarize document")

        opening_msg = [
            {
                "role": "system",
                "content": """Write a concise summary of the fragment of the video material transcription delimited by triple backquotes.
                            Keep in mind that the summary will be used as a prompt for the next step of the summarization process.""",
            },
            {
                "role": "user",
                "content": f"```{transcript[0]}```",
            },
        ]

        response = client.chat.completions.create(
            messages=opening_msg,
            model=model,
        )

        for line in transcript[1:]:
            summary_fragment = response.choices[0].message.content
            continue_message = [
                {
                    "role": "system",
                    "content": """You are given a summary of the fragment of the video material transcription delimited by triple hashtag sign.""",
                },
                {
                    "role": "user",
                    "content": f"###{summary_fragment}###",
                },
                {
                    "role": "system",
                    "content": """Write a concise summary of the video material.
                                Use the summary of the fragment before and the transcription delimited by triple backquotes.
                                Result should cover the key points of whole video material transcription.""",
                },
                {
                    "role": "user",
                    "content": f"```{line}```",
                },
            ]

            response = client.chat.completions.create(
                messages=continue_message,
                model=model,
            )

    output = response.choices[0].model_dump(
        include={
            "message": {
                "tool_calls": {
                    0: {
                        "id": True,
                        "function": {
                            "arguments": True,
                        },
                    }
                }
            }
        }
    )
    tool_call_result = json.loads(
        output["message"]["tool_calls"][0]["function"]["arguments"]
    )
    result = {
        "id": output["message"]["tool_calls"][0]["id"],
        "summary": tool_call_result["summary"],
        "tags": tool_call_result["tags"],
        "usage": {
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }

    # save result to file
    output_path = f"{'/'.join(transcription_path.split('/')[:-1])}/summary.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
