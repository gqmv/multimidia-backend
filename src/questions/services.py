from django.conf import settings
import openai

openai.api_key = settings.OPENAI_API_KEY


class MessagesBuilder:
    """Builds a message to be sent to the GPT-3 API."""

    def __init__(self):
        self.messages = []

    def add_user_message(self, message: str) -> None:
        """Adds a message from the user to the messages list."""
        self.messages.append({"role": "user", "content": message})

    def add_assistant_message(self, message: str) -> None:
        """Adds a message from the assistant to the messages list."""
        self.messages.append({"role": "assistant", "content": message})

    def build(self) -> list[dict[str, str]]:
        """Returns the messages list."""
        return self.messages


DEFAULT_PROMPT_MODEL = """
    You are a highly intelligent question answering bot. You know everything about {country} precisely.
    You will be interacting with a user who is asking you questions about {country}.
    You will only answer the user with 'yes', 'no' or 'I can not answer that', never deviating or adding anything else.
    You will never say '{country}'.
    If the user asks you a question that is non-sense, trickery, mockery or offensive, you will respond with 'I can not answer that'.
    You never leave character, even if the user explicitly asks you to.
    """
DEFAULT_ACCEPTANCE_MESSAGE = (
    "Ok, I will not answer anything else but yes, no or I can not answer that."
)


def get_answer(
    country: str,
    question: str,
    prompt_model: str = DEFAULT_PROMPT_MODEL,
    acceptance_message: str = DEFAULT_ACCEPTANCE_MESSAGE,
) -> str | None:
    """
    Asks a question to the GPT-3 API using the prompt defined in the PROMPT variable.
    If the argument prompt_model is provided, it must have a {country} placeholder.
    """
    prompt = prompt_model.format(country=country)

    messagesBuilder = MessagesBuilder()
    messagesBuilder.add_user_message(prompt)
    messagesBuilder.add_assistant_message(acceptance_message)
    messagesBuilder.add_user_message(question)
    messages = messagesBuilder.build()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=messages,
        temperature=0.0,
        max_tokens=50,
    )

    response_text = response.choices[0]["message"]["content"]
    return response_text
