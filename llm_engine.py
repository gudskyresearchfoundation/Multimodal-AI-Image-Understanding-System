import ollama
from config import LLM_MODEL


def reason_from_description(
    description: str,
    user_question: str | None = None,
    llm_model: str = LLM_MODEL,
) -> str:
    if user_question is not None and user_question.strip():
        prompt = f"""
Scene Description:
{description}

Question:
{user_question}

Answer briefly in 2-3 sentences based only on the scene description.
If the description is insufficient, say so clearly.
""".strip()
    else:
        prompt = f"""
Scene Description:
{description}

Explain briefly in 2-3 sentences what is happening in the image.
""".strip()

    response = ollama.chat(
        model=llm_model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"].strip()