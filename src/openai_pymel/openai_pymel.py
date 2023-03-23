import re
from datetime import datetime
import openai
from constants import DEFAULTS
from entry import entry_factory
from gui import OpenAIPymelGUI
# import json
# import os
# from pathlib import Path


openai.api_key = DEFAULTS.openai_key


def _timestamp():
    return datetime.now().strftime("script_%y%m%d_%H%M%S")


class OpenAIPymel:
    """OpenAIPymel OpenAI Handler"""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(OpenAIPymel, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.conversation = OpenAIPymelConversation()
        self.GUI = OpenAIPymelGUI(self)

        self.message = ""

    def completion(self, prompt: str):
        self.conversation.add_entry("sys", DEFAULTS.prompt_guide)

        response = openai.ChatCompletion.create(
            model=DEFAULTS.model,
            messages=self.conversation.log,
            stream=True,
        )

        if not response:
            return

        self.conversation.add_entry("usr", prompt)

        for chunk in response:
            if not chunk:
                continue

            content = chunk["choices"][0]["delta"].get("content", "")
            if not content:
                continue

            self.message += content
            yield self.message

        return self.message

    def parse_completion(self, response: str):
        pattern = r"```python([\s\S]*?)```"

        self.codelist = re.findall(pattern, response)
        for i, code in enumerate(self.codelist):
            self.codelist[i] = re.sub(r"\A[\r?\n]", "", code)
            self.codelist[i] = re.sub(r"[\r?\n]\Z", "", code)

    def _reset(self):
        self.conversation.clear_conversation()
        self.message = ""

    def _export(self):
        timestamp = _timestamp()

        for i, code in enumerate(self.codelist):
            codefile = DEFAULTS.script_export_bin / f"{timestamp}_{i:02d}.py"

            with codefile.open(mode="w", encoding="utf-8-sig") as f:
                f.writelines(code)

    def _call(self):
        self.GUI.call()


class OpenAIPymelConversation:
    """
    Class for OpenAIPymelConversation
    messages stored as [timestamp:{prompt:"", response:"", tokens:##}]

    """

    def __init__(self):
        self.log = []
        self.fileID = ""  # (hash)

    def clear_conversation(self):
        self.log = []

    def save_conversation(self):
        ...

    def load_conversation(self):
        ...

    def add_entry(self, mode, entry):
        row = {_timestamp(): entry_factory.get(mode, "usr")(entry)}
        self.log.append(row)


def main():
    op = OpenAIPymel()
    print(op)


if __name__ == "__main__":
    main()
