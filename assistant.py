from collections.abc import Iterator

from google import genai
from google.genai import types


def get_reply_stream(
    history: list[dict[str, str]],
    instructions: str,
    model: str,
    api_key: str,
) -> Iterator[str]:
    """Yield response text as Gemini generates it."""
    contents = [
        types.Content(
            role="user" if item["role"] == "user" else "model",
            parts=[types.Part.from_text(text=item["content"])],
        )
        for item in history[-12:]
        if item.get("role") in {"user", "assistant"} and item.get("content")
    ]

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=120_000,
        ),
    )
    response_stream = client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=instructions,
            temperature=0.25,
            max_output_tokens=1024,
            thinking_config=types.ThinkingConfig(thinking_level="low"),
        ),
    )
    for chunk in response_stream:
        if chunk.text:
            yield chunk.text
