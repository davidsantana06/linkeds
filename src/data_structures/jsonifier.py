from abc import ABC, abstractmethod
from os import path, getcwd
import json


class InvalidJsonException(Exception):
    '''Exception raised for invalid JSON.'''

    def __init__(self, message: str = 'Invalid JSON') -> None:
        super().__init__(message)


class Jsonifier(ABC):
    '''
    Abstract base class for handling JSON data.
    '''

    JSON_INDENT = 4

    def _read_json_file(self, file_path: str, encoding: str) -> object:
        '''Reads JSON data from a file.'''
        with open(file_path, 'r', encoding=encoding) as json_file:
            data = json.load(json_file)
        return data

    @abstractmethod
    def load_json(self, file_path: str = None, encoding: str = None) -> None:
        '''Abstract method to load JSON data from a file.'''
        ...

    def _read_json_str(self, json_str: str) -> object:
        '''Reads JSON data from a string.'''
        return json.loads(json_str)

    @abstractmethod
    def loads_json(self, json_str: str) -> None:
        '''Abstract method to load JSON data from a string.'''
        ...

    def _generate_file_path(self, file_path: str) -> str:
        '''Generates a valid file path for writing JSON data.'''
        if not (file_path and file_path.endswith('.json')):
            file_path = path.join(getcwd(), f'{self.__class__.__name__}.json')
        return file_path

    def _write_json_file(self, data: object, file_path: str, indent: int, encoding: str) -> None:
        '''Writes JSON data to a file.'''
        with open(self._generate_file_path(file_path), 'w', encoding=encoding) as json_file:
            json.dump(data, json_file, indent=indent)

    @abstractmethod
    def dump_json(self, file_path: str = None, indent: int = JSON_INDENT, encoding: str = None) -> None:
        '''Abstract method to dump JSON data to a file.'''
        ...

    def _write_json_str(self, data: object, indent: int = JSON_INDENT) -> str:
        '''Converts JSON data to a formatted string.'''
        return json.dumps(data, indent=indent)

    @abstractmethod
    def dumps_json(self) -> str:
        '''Abstract method to convert JSON data to a string.'''
        ...
