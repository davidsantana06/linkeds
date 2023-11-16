from abc import ABC, abstractmethod
from .node import SingleNode


class EmptyQueueException(Exception):
    def __init__(self, message: str = 'Queue is empty') -> None:
        super().__init__(message)


class FullQueueException(Exception):
    def __init__(self, message: str = 'Queue is full') -> None:
        super().__init__(message)


class Queue(ABC):
    def __init__(self) -> None:
        self._front = self._rear = None
        self._size = 0

    @property
    def size(self) -> int:
        return self._size
    
    def is_empty(self) -> bool:
        return self._size == 0

    def _enqueue(self, data: object) -> None:
        node = SingleNode(data)

        if self.is_empty():
            self._front = self._rear = node
        else:
            self._rear.next = node
            self._rear = node

        self._size += 1

    @abstractmethod
    def enqueue(self, data: object) -> None:
        ...

    def dequeue(self) -> object:
        if self.is_empty():
            raise EmptyQueueException()
        else:
            data = self._front.data
            self._front = self._front.next
            self._size -= 1

            if self.is_empty():
                self._rear = None

            return data

    def peek(self) -> object:
        return self._front.data if (self._front is not None) else self._front
    

class BoundedQueue(Queue):
    def __init__(self, capacity: int = 10) -> None:
        super().__init__()
        self.__capacity = capacity

    def is_full(self) -> bool:
        return self._size == self.__capacity
    
    def enqueue(self, data: object) -> None:
        if self.is_full():
            raise FullQueueException()
        else:
            self._enqueue(data)
        

class DynamicQueue(Queue):
    def enqueue(self, data: object) -> None:
        self._enqueue(data)
