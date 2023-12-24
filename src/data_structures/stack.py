from abc import ABC, abstractmethod
from .node import SingleNode


class EmptyStackException(Exception):
    '''Exception raised for attempting operations on an empty stack.'''

    def __init__(self, message: str = 'Stack is empty') -> None:
        super().__init__(message)


class FullStackException(Exception):
    '''Exception raised for attempting to push into a full stack.'''

    def __init__(self, message: str = 'Stack is full') -> None:
        super().__init__(message)


class LinkedStack(ABC):
    '''Abstract base class for a linked stack.'''

    def __init__(self) -> None:
        '''Initializes an empty linked stack.'''
        self._top = None
        self._size = 0

    @property
    def size(self) -> int:
        '''Getter method for the size attribute.'''
        return self._size

    def is_empty(self) -> bool:
        '''Checks if the stack is empty.'''
        return self._size == 0

    def _push(self, data: object) -> None:
        '''Internal method to push a new node with the given data onto the stack.'''
        self._top = SingleNode(data, self._top)
        self._size += 1

    @abstractmethod
    def push(self, data: object) -> None:
        '''Abstract method to push data onto the stack.'''
        ...

    def pop(self) -> object:
        '''
        Removes and returns the top element from the stack.

        Raises:
            EmptyStackException: If the stack is empty.
        '''
        if self.is_empty():
            raise EmptyStackException()

        data = self._top.data
        self._top = self._top.next
        self._size -= 1

        return data

    def peek(self) -> object:
        '''
        Returns the data of the top element without removing it.

        Returns:
            object: Data of the top element, or None if the stack is empty.
        '''
        return self._top.data if (self._top is not None) else self._top


class BoundedStack(LinkedStack):
    '''Class representing a bounded (fixed-size) stack.'''

    def __init__(self, capacity: int = 10) -> None:
        '''
        Initializes a bounded stack with the given capacity.

        Parameters:
            capacity (int): Maximum capacity of the stack.
        '''
        super().__init__()
        self._capacity = capacity
    
    def is_full(self) -> bool:
        '''Checks if the stack is full.'''
        return self._size == self._capacity
    
    def push(self, data: object) -> None:
        '''
        Pushes data onto the stack.

        Raises:
            FullStackException: If the stack is full.
        '''
        if self.is_full():
            raise FullStackException()

        self._push(data)


class DynamicStack(LinkedStack):
    '''Class representing a dynamic (unbounded) stack.'''

    def push(self, data: object) -> None:
        '''Pushes data onto the stack.'''
        self._push(data)
