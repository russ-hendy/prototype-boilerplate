# Handle API calls to OpenAI

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Basic completion - no streaming
async def generate_completion(prompt: str, model: str = "gpt-4") -> str:
    """Generate a completion using OpenAI."""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# streamed completion
def generate_completion_stream(prompt: str, model: str = "gpt-4"):
    """Generate a streaming completion using OpenAI."""
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content