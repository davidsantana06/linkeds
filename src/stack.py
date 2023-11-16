from abc import ABC, abstractmethod
from .node import SingleNode


class EmptyStackException(Exception):
    def __init__(self, message: str = 'Stack is empty') -> None:
        super().__init__(message)


class FullStackException(Exception):
    def __init__(self, message: str = 'Stack is full') -> None:
        super().__init__(message)


class Stack(ABC):
    def __init__(self) -> None:
        self._top = None
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def _push(self, data: object) -> None:
        self._top = SingleNode(data, self._top)
        self._size += 1

    @abstractmethod
    def push(self, data: object) -> None:
        ...

    def pop(self) -> object:
        if self.is_empty():
            raise EmptyStackException()
        else:
            data = self._top.data
            self._top = self._top.next
            self._size -= 1

            return data

    def peek(self) -> object:
        return self._top.data if (self._top is not None) else self._top


class BoundedStack(Stack):
    def __init__(self, capacity: int = 10) -> None:
        super().__init__()
        self.__capacity = capacity
    
    def is_full(self) -> bool:
        return self._size == self.__capacity
    
    def push(self, data: object) -> None:
        if self.is_full():
            raise FullStackException()
        else:
            self._push(data)


class DynamicStack(Stack):
    def push(self, data: object) -> None:
        self._push(data)
