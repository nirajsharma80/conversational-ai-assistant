from google import genai
from google.genai import types


def get_reply(
    history: list[dict[str, str]],
    instructions: str,
    model: str,
    api_key: str,
) -> str:
    """Generate a response from the recent conversation using Gemini."""
    contents = [
        types.Content(
            role="user" if item["role"] == "user" else "model",
            parts=[types.Part.from_text(text=item["content"])],
        )
        for item in history[-12:]
        if item.get("role") in {"user", "assistant"} and item.get("content")
    ]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=instructions,
            temperature=0.25,
            max_output_tokens=1024,
        ),
    )
    return (response.text or "I couldn’t generate a text response. Please try again.").strip()
