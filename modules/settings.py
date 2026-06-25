"""
=========================================================
ASV Manager
Settings
=========================================================
"""

import json
import os


SETTINGS_FILE = "settings.json"


class Settings:

    def __init__(self):

        self.data = {
            "last_excel": "",
            "last_kw": ""
        }

        self.load()

    def load(self):

        if os.path.exists(SETTINGS_FILE):

            with open(
                SETTINGS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                self.data = json.load(f)

    def save(self):

        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.data,
                f,
                indent=4,
                ensure_ascii=False
            )

    def get(self, key):

        return self.data.get(key, "")

    def set(self, key, value):

        self.data[key] = value
        self.save()