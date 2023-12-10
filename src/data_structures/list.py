from abc import ABC, abstractmethod
from typing import Iterator, List, Tuple, Set, Union

from .jsonifier import Jsonifier
from .node import DoubleNode


class EmptyListException(Exception):
    '''Exception raised for attempting operations on an empty linked list.'''

    def __init__(self, message: str = 'List is empty') -> None:
        super().__init__(message)


class FullListException(Exception):
    '''Exception raised for attempting operations on a full linked list.'''

    def __init__(self, message: str = 'List is full') -> None:
        super().__init__(message)


class IndexListError(IndexError):
    '''Exception raised for index-related errors in linked lists.'''

    def __init__(self, message: str = 'List index out of range') -> None:
        super().__init__(message)


class InvalidIterableAssignmentException(Exception):
    '''Exception raised for invalid iterable assignments to a linked list.'''

    def __init__(self, message: str = 'Iterable must be a list, tuple, or set') -> None:
        super().__init__(message)


class LinkedList(ABC):
    '''Abstract base class for a doubly linked list.'''

    ASSIGNABLE_ITERABLE_TYPES = (list, tuple, set)

    def __init__(self) -> None:
        '''Initializes an empty linked list.'''
        self._head = self._tail = None
        self._size = 0

    @property
    def size(self) -> int:
        '''Getter method for the size attribute.'''
        return self._size
    
    def is_empty(self) -> bool:
        '''Checks if the list is empty.'''
        return self._size == 0
    
    def _add_first(self, data: object) -> None:
        '''Internal method to add a new node with the given data to the beginning of the list.'''
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
        '''Abstract method to add data to the beginning of the list.'''
        ...

    def _add_last(self, data: object) -> None:
        '''Internal method to add a new node with the given data to the end of the list.'''
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
        '''Abstract method to add data to the end of the list.'''
        ...

    def _insert(self, index: int, data: object) -> None:
        '''
        Internal method to insert a new node with the given data at the specified index.

        Raises:
            IndexListError: If the index is out of range.
        '''
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
        '''Abstract method to insert data at the specified index.'''
        ...

    def get_first(self) -> object:
        '''Returns the data of the first element in the list.'''
        return self._head.data if (self._head is not None) else self._head
    
    def get_last(self) -> object:
        '''Returns the data of the last element in the list.'''
        return self._tail.data if (self._tail is not None) else self._tail

    def get(self, index: int) -> object:
        '''
        Returns the data of the element at the specified index.

        Raises:
            IndexListError: If the index is out of range.
        '''
        if index < 0 or index >= self._size:
            raise IndexListError()
        else:
            node = self._head

            for _ in range(index):
                node = node.next

            return node.data

    def remove_first(self) -> object:
        '''
        Removes and returns the data of the first element in the list.

        Raises:
            EmptyListException: If the list is empty.
        '''
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
        '''
        Removes and returns the data of the last element in the list.

        Raises:
            EmptyListException: If the list is empty.
        '''
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
        '''
        Removes and returns the data of the element at the specified index.

        Raises:
            EmptyListException: If the list is empty.
            IndexListError: If the index is out of range.
        '''
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
        
    def _reverse(self, **kwargs) -> 'LinkedList':
        '''Internal method to create and return a new reversed linked list.'''
        reverse_list = self.__class__(**kwargs)
        node = self._tail

        while node is not None:
            reverse_list.add_last(node.data)
            node = node.prev

        return reverse_list

    @abstractmethod
    def reverse(self) -> 'LinkedList':
        '''Abstract method to create and return a new reversed linked list.'''
        ...

    @abstractmethod
    def assign_iterable(self, iterable: Union[List[object], Tuple[object], Set[object]]) -> None:
        '''Abstract method to assign data from an iterable to the linked list.'''
        ...

    def to_list(self) -> List[object]:
        '''Converts the linked list to a Python list.'''
        return list(self)

    def to_tuple(self) -> Tuple[object]:
        '''Converts the linked list to a Python tuple.'''
        return tuple(self)

    def to_set(self) -> Set[object]:
        '''Converts the linked list to a Python set.'''
        return set(self)

    def __iter__(self) -> Iterator[object]:
        '''Iterator method to allow iterating through the elements of the linked list.'''
        node = self._head

        while node is not None:
            yield node.data
            node = node.next


class BoundedList(LinkedList, Jsonifier):
    '''Class representing a bounded linked list with additional JSON serialization functionality.'''

    def __init__(self, capacity: int = 10) -> None:
        '''
        Initializes a bounded linked list with the given capacity.

        Parameters:
            capacity (int): Maximum capacity of the list.
        '''
        LinkedList.__init__(self)
        self._capacity = capacity

    def is_full(self) -> bool:
        '''Checks if the list is full.'''
        return self._size == self._capacity
    
    def add_first(self, data: object) -> None:
        '''
        Adds data to the beginning of the list.

        Raises:
            FullListException: If the list is full.
        '''
        if self.is_full():
            raise FullListException()
        else:
            self._add_first(data)

    def add_last(self, data: object) -> None:
        '''
        Adds data to the end of the list.

        Raises:
            FullListException: If the list is full.
        '''
        if self.is_full():
            raise FullListException()
        else:
            self._add_last(data)

    def insert(self, index: int, data: object) -> None:
        '''
        Inserts data at the specified index.

        Raises:
            FullListException: If the list is full.
        '''
        if self.is_full():
            raise FullListException()
        else:
            self._insert(index, data)

    def reverse(self) -> 'BoundedList':
        '''Creates and returns a new reversed bounded linked list.'''
        return self._reverse(capacity=self._capacity)

    def assign_iterable(self, iterable: Union[List[object], Tuple[object], Set[object]]) -> None:
        '''
        Assigns data from an iterable to the linked list.

        Raises:
            InvalidIterableAssignmentException: If the iterable type is not supported.
        '''
        if type(iterable) not in self.ASSIGNABLE_ITERABLE_TYPES:
            raise InvalidIterableAssignmentException()
        else:
            self._head = self._tail = None
            self._size = 0
            self._capacity = len(iterable)

            for item in iterable:
                self.add_last(item)
    
    def load_json(self, file_path: str = None, encoding: str = None) -> None:
        '''Loads data from a JSON file into the linked list.'''
        self.assign_iterable(self._read_json_file(file_path, encoding))

    def loads_json(self, json_str: str) -> None:
        '''Loads data from a JSON string into the linked list.'''
        self.assign_iterable(self._read_json_str(json_str))

    def dump_json(self, file_path: str = None, indent: int = Jsonifier.JSON_INDENT, encoding: str = None) -> None:
        '''Writes the linked list data to a JSON file.'''
        self._write_json_file(self.to_list(), file_path, indent, encoding)

    def dumps_json(self, indent: int = Jsonifier.JSON_INDENT) -> str:
        '''Returns a JSON string representation of the linked list.'''
        return self._write_json_str(self.to_list(), indent)


class DynamicList(LinkedList, Jsonifier):
    '''Class representing a dynamic linked list with additional JSON serialization functionality.'''

    def add_first(self, data: object) -> None:
        '''Adds data to the beginning of the list.'''
        self._add_first(data)
    
    def add_last(self, data: object) -> None:
        '''Adds data to the end of the list.'''
        self._add_last(data)
    
    def insert(self, index: int, data: object) -> None:
        '''Inserts data at the specified index.'''
        self._insert(index, data)

    def reverse(self) -> 'DynamicList':
        '''Creates and returns a new reversed dynamic linked list.'''
        return self._reverse()
    
    def assign_iterable(self, iterable: Union[List[object], Tuple[object], Set[object]]) -> None:
        '''
        Assigns data from an iterable to the linked list.

        Raises:
            InvalidIterableAssignmentException: If the iterable type is not supported.
        '''
        if type(iterable) not in self.ASSIGNABLE_ITERABLE_TYPES:
            raise InvalidIterableAssignmentException()
        else:
            self._head = self._tail = None
            self._size = 0

            for item in iterable:
                self.add_last(item)
    
    def load_json(self, file_path: str = None, encoding: str = None) -> None:
        '''Loads data from a JSON file into the linked list.'''
        self.assign_iterable(self._read_json_file(file_path, encoding))

    def loads_json(self, json_str: str) -> None:
        '''Loads data from a JSON string into the linked list.'''
        self.assign_iterable(self._read_json_str(json_str))

    def dump_json(self, file_path: str = None, indent: int = Jsonifier.JSON_INDENT, encoding: str = None) -> None:
        '''Writes the linked list data to a JSON file.'''
        self._write_json_file(self.to_list(), file_path, indent, encoding)

    def dumps_json(self, indent: int = Jsonifier.JSON_INDENT) -> str:
        '''Returns a JSON string representation of the linked list.'''
        return self._write_json_str(self.to_list(), indent)
