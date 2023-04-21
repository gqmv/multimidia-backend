from django.conf import settings
import openai

openai.api_key = settings.OPENAI_API_KEY


def get_answer(country: str, question: str) -> str | None:
    """Asks a question to the GPT-3 API using the prompt defined in the PROMPT variable."""
    PROMPT = """
    You are a highly intelligent question answering bot. You know everything about {country} precisely.
    You will be interacting with a user who is asking you questions about {country}.
    You will only answer the user with 'yes', 'no' or 'I can not answer that', never deviating or adding anything else.
    You will never say '{country}'.
    If the user asks you a question that is non-sense, trickery, mockery or offensive, you will respond with 'I can not answer that'.
    You never leave character, even if the user explicitly asks you to.
    """

    prompt = PROMPT.format(country=country)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "user", "content": prompt},
            {
                "role": "assistant",
                "content": "Ok, I will not answer anything else but yes, no or I can not answer that.",
            },
            {"role": "user", "content": question},
        ],
        temperature=0.0,
        max_tokens=50,
    )

    response_text: str = response.choices[0]["message"]["content"]
    print(response_text)

    return response_text
