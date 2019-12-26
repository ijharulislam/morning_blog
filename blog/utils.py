import inspect
from abc import ABCMeta, abstractmethod


class FormValidator:
    __metaclass__ = ABCMeta

    def __init__(self, data):
        self.data = data
        self.cleaned_data = {}
        self.errors = {}

    def is_valid(self):
        for name, validator in inspect.getmembers(self, predicate=inspect.ismethod):
            if "validate_" in name:
                validator()
        return not self.errors

    @abstractmethod
    def save(self):
        pass
