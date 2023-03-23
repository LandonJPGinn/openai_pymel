import os
from pathlib import Path

import tomllib


class DefaultLoader:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DefaultLoader, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        with open("settings.toml", "rb") as f:
            self.__dict__.update(**tomllib.load(f))
            self.openai_key = os.environ["OPENAI_KEY"]
            self.script_export_bin = Path(script_export_bin).expanduser().resolve()


DEFAULTS = DefaultLoader()
