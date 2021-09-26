from types import SimpleNamespace

from locales.ru import ru
from locales.en import en


class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)


dictionary = {"ru": NestedNamespace(ru), "en": NestedNamespace(en)}
