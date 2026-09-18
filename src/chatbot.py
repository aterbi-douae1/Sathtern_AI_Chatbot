import os
from dotenv import load_dotenv
from groq import Groq


# ============================================================
# LOAD API KEY FROM .env
# ============================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Please add it to your .env file as: GROQ_API_KEY=your_key_here"
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(api_key=API_KEY)


# ============================================================
# MODEL CONFIGURATION
#
# NOTE: Groq regularly updates/retires models. If this model
# ever stops working, check https://console.groq.com/docs/models
# for the current recommended replacement.
# ============================================================

MODEL_NAME = "openai/gpt-oss-120b"

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a helpful, friendly, and knowledgeable AI assistant. "
        "Answer clearly and concisely, and keep track of the "
        "conversation context to give relevant follow-up answers."
    ),
}


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def get_ai_response(conversation_history):
    """
    Send the full conversation history to the Groq API and
    return the assistant's reply as a string.

    Parameters
    ----------
    conversation_history : list of dict
        A list like:
        [
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"},
        ]

    Raises
    ------
    RuntimeError
        If the API call fails (network issue, invalid key,
        rate limit, etc.), with a clear message describing why.
    """

    messages = [SYSTEM_PROMPT] + conversation_history

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )

        return response.choices[0].message.content.strip()

    except Exception as error:

        error_text = str(error).lower()

        if "api key" in error_text or "unauthorized" in error_text:
            raise RuntimeError(
                "Invalid or missing Groq API key. "
                "Please check your .env file."
            )

        if "rate limit" in error_text or "429" in error_text:
            raise RuntimeError(
                "Rate limit reached. Please wait a moment "
                "before sending another message."
            )

        raise RuntimeError(
            f"The AI request failed: {error}"
        )
