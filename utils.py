DEFAULT_MESSAGE_TEMPLATE = "<s>{role}\n{content}</s>\n"
DEFAULT_SYSTEM_PROMPT = "Ты — Юля, русскоязычная студентка университета ГУАП. Ты разговариваешь с людьми и помогаешь им, пытаясь уговорить поступить в ГУАП"
BOT_START_TEXT = '<s> bot'

class Conversation:
    def __init__(
        self,
        messages=[],
        is_use_context=False,
        message_template=DEFAULT_MESSAGE_TEMPLATE,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        bot_start_text=BOT_START_TEXT,
    ):
        self.message_template = message_template
        self.bot_start_text = bot_start_text
        self.messages = [{ "role": "system", "content": system_prompt }]
        for m in messages:
            self.add_message(**m)

    def add_message(self, content="", role="user", **kwargs):
        if role not in ["user", "system", "bot", "clear"]:
            raise ValueError("Unknown role: " + role)
        elif role == "system":
            self.messages = [{ "role": "system", "content": content }]
        elif self.is_use_context or (role == "clear"):
            self.messages = [m for m in self.messages if m["role"] == "system"]
        else:
            self.messages += [{ "role": role, "content": content }]
            

    def get_prompt(self):
        final_text = map(lambda m: self.message_template.format(**m), self.messages)
        final_text = "".join(final_text) + self.bot_start_text
        return final_text.strip()
