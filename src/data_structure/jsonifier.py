from abc import ABC, abstractmethod
from os import path, getcwd
import json


class InvalidJsonException(Exception):
    def __init__(self, message: str = 'Invalid JSON') -> None:
        super().__init__(message)


class Jsonifier(ABC):
    JSON_INDENT = 4

    def _read_json_file(self, file_path: str, encoding: str) -> object:
        with open(file_path, 'r', encoding=encoding) as json_file:
            data = json.load(json_file)

        return data

    @abstractmethod
    def load_json(self, file_path: str = None, encoding: str = None) -> None:
        ...

    def _read_json_str(self, json_str: str) -> object:
        return json.loads(json_str)

    @abstractmethod
    def loads_json(self, json_str: str) -> None:
        ...

    def _generate_file_path(self, file_path: str) -> str:
        if not (file_path and file_path.endswith('.json')):
            file_path = path.join(getcwd(), f'{self.__class__.__name__}.json')

        return file_path

    def _write_json_file(self, data: object, file_path: str, indent: int, encoding: str) -> None:
        with open(self._generate_file_path(file_path), 'w', encoding=encoding) as json_file:
            json.dump(data, json_file, indent=indent)

    @abstractmethod
    def dump_json(self, file_path: str = None, indent: int = JSON_INDENT, encoding: str = None) -> None:
        ...
    
    def _write_json_str(self, data: object, indent: int = JSON_INDENT) -> str:
        return json.dumps(data, indent=indent)

    @abstractmethod
    def dumps_json(self) -> str:
        ...
