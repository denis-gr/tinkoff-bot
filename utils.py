import os

DEFAULT_MESSAGE_TEMPLATE = "<s>{role}\n{content}</s>\n"
DEFAULT_SYSTEM_PROMPT = "Ты — Агафья, русскоязычная студентка университета ГУАП. Ты разговариваешь с людьми и помогаешь им, пытаясь уговорить поступить в ГУАП"
DEFAULT_BOT_START_TEXT = '<s> bot'

IS_USE_CONTEXT = os.environ.get("BOT_IS_USE_CONTEXT", False)
MESSAGE_TEMPLATE = os.environ.get("BOT_MESSAGE_TEMPLATE", DEFAULT_MESSAGE_TEMPLATE)
SYSTEM_PROMPT = os.environ.get("BOT_SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)
BOT_START_TEXT = os.environ.get("BOT_BOT_START_TEXT", DEFAULT_BOT_START_TEXT)

class Conversation:
    def __init__(
        self,
        messages=[],
        is_use_context=IS_USE_CONTEXT,
        message_template=MESSAGE_TEMPLATE,
        system_prompt=SYSTEM_PROMPT,
        bot_start_text=BOT_START_TEXT,
    ):
        self.message_template = message_template
        self.bot_start_text = bot_start_text
        self.is_use_context = is_use_context in [True, "True"]
        self.messages = [{ "role": "system", "content": system_prompt }]
        for m in messages:
            self.add_message(**m)

    def add_message(self, content="", role="user", **kwargs):
        if role not in ["user", "system", "bot", "clear"]:
            raise ValueError("Unknown role: " + role)
        elif role == "system":
            self.messages = [{ "role": "system", "content": content }]
        elif role == "clear":
            self.messages = [m for m in self.messages if m["role"] == "system"]
        elif not self.is_use_context:
            self.messages = [m for m in self.messages if m["role"] == "system"]
            self.messages += [{ "role": role, "content": content }]
        else:
            self.messages += [{ "role": role, "content": content }]
            

    def get_prompt(self):
        final_text = map(lambda m: self.message_template.format(**m), self.messages)
        final_text = "".join(final_text) + self.bot_start_text
        return final_text.strip()
