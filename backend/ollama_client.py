import ollama
import time
import json

from structured_output_schema import (
    StructuredLLMResponse
)

MAX_RETRIES = 3


def generate_response(
    model,
    prompt,
    temperature=0
):

    structured_prompt = f"""
You are an AI assistant.

Return ONLY valid JSON.

Do not explain anything.
Do not return markdown.
Do not use triple backticks.

Required schema:

{{
    "topic": "string",
    "definition": "string",
    "key_points": ["string"],
    "example": "string"
}}

User Question:
{prompt}
"""

    attempt = 0

    while attempt < MAX_RETRIES:

        try:
            start_time = time.time()

            stream = ollama.chat(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": structured_prompt
                    }
                ],
                options={
                    "temperature": temperature
                },
                stream=True
            )

            full_response = ""
            first_token_time = None

            for chunk in stream:

                content = (
                    chunk["message"]
                    .get("content", "")
                )

                if content:

                    if first_token_time is None:
                        first_token_time = (
                            time.time()
                        )

                    full_response += content

            end_time = time.time()

            inference_time = round(
                end_time - start_time,
                2
            )

            ttft = round(
                (
                    first_token_time -
                    start_time
                ),
                2
            ) if first_token_time else inference_time

            cleaned_response = (
                full_response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            parsed_json = json.loads(
                cleaned_response
            )

            validated_response = (
                StructuredLLMResponse(
                    **parsed_json
                )
            )

            return {
                "response":
                    validated_response.model_dump(),

                "ttft":
                    ttft,

                "inference_time":
                    inference_time,

                "valid_output":
                    True,

                "retry_count":
                    attempt
            }

        except Exception:

            attempt += 1

    return {
        "response": {
            "topic":
                "Generation Failed",

            "definition":
                "Model failed to return valid structured JSON.",

            "key_points": [],

            "example": ""
        },

        "ttft": 0,

        "inference_time": 0,

        "valid_output": False,

        "retry_count": MAX_RETRIES
    }