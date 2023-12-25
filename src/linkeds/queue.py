from abc import ABC, abstractmethod
from .node import SingleNode


class EmptyQueue(Exception):
    '''Exception raised for attempting operations on an empty queue.'''

    def __init__(self, message: str = 'Queue is empty') -> None:
        super().__init__(message)


class FullQueue(Exception):
    '''Exception raised for attempting to enqueue into a full queue.'''

    def __init__(self, message: str = 'Queue is full') -> None:
        super().__init__(message)


class LinkedQueue(ABC):
    '''Abstract base class for a linked queue.'''

    def __init__(self) -> None:
        '''Initializes an empty linked queue.'''
        self._front = self._rear = None
        self._size = 0

    @property
    def size(self) -> int:
        '''Getter method for the size attribute.'''
        return self._size
    
    def is_empty(self) -> bool:
        '''Checks if the queue is empty.'''
        return self._size == 0

    def _enqueue(self, data: object) -> None:
        '''Internal method to enqueue a new node with the given data.'''
        node = SingleNode(data)
        if self.is_empty():
            self._front = self._rear = node
        else:
            self._rear.next = node
            self._rear = node
        self._size += 1

    @abstractmethod
    def enqueue(self, data: object) -> None:
        '''Abstract method to enqueue data into the queue.'''
        ...

    def dequeue(self) -> object:
        '''
        Removes and returns the front element from the queue.
        
        Raises:
            EmptyQueue: If the queue is empty.
        '''
        if self.is_empty():
            raise EmptyQueue()

        data = self._front.data
        self._front = self._front.next
        self._size -= 1
        if self.is_empty():
            self._rear = None
        return data

    def peek(self) -> object:
        '''
        Returns the data of the front element without removing it.

        Returns:
            object: Data of the front element, or None if the queue is empty.
        '''
        return self._front.data if (self._front is not None) else self._front
    

class BoundedQueue(LinkedQueue):
    '''Class representing a bounded (fixed-size) queue.'''

    def __init__(self, capacity: int = 10) -> None:
        '''
        Initializes a bounded queue with the given capacity.

        Parameters:
            capacity (int): Maximum capacity of the queue.
        '''
        super().__init__()
        self._capacity = capacity

    def is_full(self) -> bool:
        '''Checks if the queue is full.'''
        return self._size == self._capacity
    
    def enqueue(self, data: object) -> None:
        '''
        Enqueues data into the queue.

        Raises:
            FullQueue: If the queue is full.
        '''
        if self.is_full():
            raise FullQueue()

        self._enqueue(data)


class DynamicQueue(LinkedQueue):
    '''Class representing a dynamic (unbounded) queue.'''

    def enqueue(self, data: object) -> None:
        '''Enqueues data into the queue.'''
        self._enqueue(data)
