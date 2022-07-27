import os
import os.path
import json


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Locale(metaclass=Singleton):
    locale_folder = 'locales'

    def __init__(self):
        self.lang = None
        self.locale_strings = {}

    def set_language(self, lang):
        self.lang = lang
        try:
            with open(os.path.join(self.locale_folder, f'{lang}.json')) as f:
                self.locale_strings = json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Language {lang} is not supported")

    def langs(self):
        return [f.removesuffix('.json') for f in os.listdir(self.locale_folder) if f.endswith('.json')]

    def __getattr__(self, key):
        assert self.lang is not None, "Run `locale.set_language(<lang_code>)` to start"
        assert key in self.locale_strings, "No such string"
        return self.locale_strings[key]