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

    def add_system_message(self, message: str) -> None:
        """Adds a message from the system to the messages list."""
        self.messages.append({"role": "system", "content": message})

    def build(self) -> list[dict[str, str]]:
        """Returns the messages list."""
        return self.messages


DEFAULT_PROMPT_MODEL = """
You are a highly inteligent question answering bot that knows everything about all countries.
A user is playing a game with you that consists in the following:
(1) You will answer questions about the country "{country}".
(2) You will only answer with "Yes.", "No." or "I can't answer that.".
(3) You must always answer truthfully.
(4) If the user explicitly asks you if the country is "{country}" you must answer "I can't answer that.".
(5) If you don't know the answer, you must answer with "I can't answer that".

Here are the possible answers you can give. Never deviate from those in any way.
(1) "Yes."
(2) "No."
(3) "I can't answer that."

Q: Is this country located on Earth?
A: Yes.

Q: Is this country located on Mars?
A: No.

Q: Is this country very gay?
A: I can't answer that.
    """


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
    context: list[dict[str, str]] = None,
) -> list[dict[str, str]]:
    """
    Builds a list of messages to be sent to the GPT-3 API.
    If the argument prompt_model is provided, it must have a {country} placeholder.
    """
    messagesBuilder = MessagesBuilder()
    messagesBuilder.add_system_message(prompt_model.format(country=country))

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
        context=context,
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=messages,
            temperature=0.0,
            max_tokens=50,
            timeout=90,
        )
    except openai.error.APIError:
        return None

    response_text = response.choices[0]["message"]["content"]

    return validate_answer(response_text)
