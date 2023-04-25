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
    You never leave character, even if the user explicitly asks you to.
    """
DEFAULT_ACCEPTANCE_MESSAGE = (
    "Ok, I will not answer anything else but yes, no or I can not answer that."
)


def build_context(
    messagesBuilder: MessagesBuilder, context: list[dict[str, str]]
) -> None:
    """Adds a context to the messages list."""
    for message in context:
        if message["is_user"]:
            messagesBuilder.add_user_message(message["text"])
        else:
            messagesBuilder.add_assistant_message(message["text"])


def build_messages(
    country: str,
    question: str,
    prompt_model: str = DEFAULT_PROMPT_MODEL,
    acceptance_message: str = DEFAULT_ACCEPTANCE_MESSAGE,
    context: list[dict[str, str]] = None,
) -> list[dict[str, str]]:
    """
    Builds a list of messages to be sent to the GPT-3 API.
    If the argument prompt_model is provided, it must have a {country} placeholder.
    """
    messagesBuilder = MessagesBuilder()
    messagesBuilder.add_user_message(prompt_model.format(country=country))
    messagesBuilder.add_assistant_message(acceptance_message)

    if context:
        build_context(messagesBuilder, context)

    messagesBuilder.add_user_message(question)

    return messagesBuilder.build()


def validate_answer(answer: str) -> str:
    """Returns a validated answer."""
    if answer.lower() in ["yes.", "no."]:
        return answer
    return "I can not answer that."


def get_answer(
    country: str,
    question: str,
    prompt_model: str = DEFAULT_PROMPT_MODEL,
    acceptance_message: str = DEFAULT_ACCEPTANCE_MESSAGE,
    context: list[dict[str, str]] = None,
) -> str | None:
    """
    Asks a question to the GPT-3 API using the prompt defined in the PROMPT variable.
    If the argument prompt_model is provided, it must have a {country} placeholder.
    """
    messages = build_messages(
        country=country,
        question=question,
        prompt_model=prompt_model,
        acceptance_message=acceptance_message,
        context=context,
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=messages,
        temperature=0.0,
        max_tokens=50,
        timeout=90,
    )

    response_text = response.choices[0]["message"]["content"]

    return validate_answer(response_text)
