from abc import ABC, abstractmethod
from typing import Iterator, List, Tuple, Set, Union

from .jsonifier import Jsonifier, InvalidJsonException
from .node import DoubleNode


class EmptyListException(Exception):
    def __init__(self, message: str = 'List is empty') -> None:
        super().__init__(message)


class FullListException(Exception):
    def __init__(self, message: str = 'List is full') -> None:
        super().__init__(message)


class IndexListError(IndexError):
    def __init__(self, message: str = 'List index out of range') -> None:
        super().__init__(message)


class LinkedList(ABC):
    ASSIGNABLE_ITERABLE_TYPES = (list, tuple, set) 

    def __init__(self) -> None:
        self._head = self._tail = None
        self._size = 0

    @property
    def size(self) -> int:
        return self._size
    
    def is_empty(self) -> bool:
        return self._size == 0
    
    def _add_first(self, data: object) -> None:
        node = DoubleNode(data)

        if self.is_empty():
            self._head = self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node

        self._size += 1

    @abstractmethod
    def add_first(self, data: object) -> None:
        ...

    def _add_last(self, data: object) -> None:
        node = DoubleNode(data)

        if self.is_empty():
            self._head = self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node

        self._size += 1

    @abstractmethod
    def add_last(self, data: object) -> None:
        ...

    def _insert(self, index: int, data: object) -> None:
        if index < 0 or index > self._size:
            raise IndexListError()
        elif index == 0:
            self.add_first(data)
        elif index == self._size:
            self.add_last(data)
        else:
            node = DoubleNode(data)
            current = self._head

            for _ in range(index):
                current = current.next

            node.next = current
            node.prev = current.prev
            current.prev.next = node
            current.prev = node

            self._size += 1

    @abstractmethod
    def insert(self, index: int, data: object) -> None:
        ...

    def get_first(self) -> object:
        return self._head.data if (self._head is not None) else self._head
    
    def get_last(self) -> object:
        return self._tail.data if (self._tail is not None) else self._tail

    def get(self, index: int) -> object:
        if index < 0 or index >= self._size:
            raise IndexListError()
        else:
            node = self._head

            for _ in range(index):
                node = node.next

            return node.data

    def remove_first(self) -> object:
        if self.is_empty():
            raise EmptyListException()
        else:
            data = self._head.data

            if self._head is self._tail:
                self._head = self._tail = None
            else:
                self._head = self._head.next
                self._head.prev = None

            self._size -= 1

            return data
        
    def remove_last(self) -> object:
        if self.is_empty():
            raise EmptyListException()
        else:
            data = self._tail.data

            if self._head is self._tail:
                self._head = self._tail = None
            else:
                self._tail = self._tail.prev
                self._tail.next = None

            self._size -= 1

            return data
        
    def remove(self, index: int) -> object:
        if self.is_empty():
            raise EmptyListException()
        elif index < 0 or index >= self._size:
            raise IndexListError()
        else:
            if index == 0:
                data = self.remove_first()
            elif index == self._size - 1:
                data = self.remove_last()
            else:
                node = self._head

                for _ in range(index):
                    node = node.next

                data = node.data
                node.prev.next = node.next
                node.next.prev = node.prev

                self._size -= 1

            return data
        
    def _reverse(self, **kwargs) -> 'List':
        reverse_list = self.__class__(**kwargs)
        node = self._tail

        while node is not None:
            reverse_list.add_last(node.data)
            node = node.prev

        return reverse_list

    @abstractmethod
    def reverse(self) -> 'List':
        ...

    @abstractmethod
    def assign_iterable(self, iterable: Union[List[object], Tuple[object], Set[object]]) -> None:
        ...

    def to_list(self) -> List[object]:
        return list(self)

    def to_tuple(self) -> Tuple[object]:
        return tuple(self)

    def to_set(self) -> Set[object]:
        return set(self)

    def __iter__(self) -> Iterator[object]:
        node = self._head

        while node is not None:
            yield node.data
            node = node.next


class BoundedList(LinkedList, Jsonifier):
    def __init__(self, capacity: int = 10) -> None:
        LinkedList.__init__(self)
        self._capacity = capacity

    def is_full(self) -> bool:
        return self._size == self._capacity
    
    def add_first(self, data: object) -> None:
        if self.is_full():
            raise FullListException()
        else:
            self._add_first(data)

    def add_last(self, data: object) -> None:
        if self.is_full():
            raise FullListException()
        else:
            self._add_last(data)

    def insert(self, index: int, data: object) -> None:
        if self.is_full():
            raise FullListException()
        else:
            self._insert(index, data)

    def reverse(self) -> 'BoundedList':
        return self._reverse(capacity=self._capacity)

    def assign_iterable(self, iterable: Union[List[object], Tuple[object], Set[object]]) -> None:
        if type(iterable) not in self.ASSIGNABLE_ITERABLE_TYPES:
            raise InvalidJsonException()
        else:
            self._head = self._tail = None
            self._size = 0
            self._capacity = len(iterable)

            for item in iterable:
                self.add_last(item)
    
    def load_json(self, file_path: str = None, encoding: str = None) -> None:
        self.assign_iterable(self._read_json_file(file_path, encoding))

    def loads_json(self, json_str: str) -> None:
        self.assign_iterable(self._read_json_str(json_str))

    def dump_json(self, file_path: str = None, indent: int = Jsonifier.JSON_INDENT, encoding: str = None) -> None:
        self._write_json_file(self.to_list(), file_path, indent, encoding)

    def dumps_json(self, indent: int = Jsonifier.JSON_INDENT) -> str:
        return self._write_json_str(self.to_list(), indent)


class DynamicList(LinkedList, Jsonifier):
    def add_first(self, data: object) -> None:
        self._add_first(data)
    
    def add_last(self, data: object) -> None:
        self._add_last(data)
    
    def insert(self, index: int, data: object) -> None:
        self._insert(index, data)

    def reverse(self) -> 'DynamicList':
        return self._reverse()
    
    def assign_iterable(self, iterable: Union[List[object], Tuple[object], Set[object]]) -> None:
        if type(iterable) not in self.ASSIGNABLE_ITERABLE_TYPES:
            raise InvalidJsonException()
        else:
            self._head = self._tail = None
            self._size = 0

            for item in iterable:
                self.add_last(item)
    
    def load_json(self, file_path: str = None, encoding: str = None) -> None:
        self.assign_iterable(self._read_json_file(file_path, encoding))

    def loads_json(self, json_str: str) -> None:
        self.assign_iterable(self._read_json_str(json_str))

    def dump_json(self, file_path: str = None, indent: int = Jsonifier.JSON_INDENT, encoding: str = None) -> None:
        self._write_json_file(self.to_list(), file_path, indent, encoding)

    def dumps_json(self, indent: int = Jsonifier.JSON_INDENT) -> str:
        return self._write_json_str(self.to_list(), indent)
