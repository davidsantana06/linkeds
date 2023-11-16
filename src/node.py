from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self, data: object, next: 'Node' = None) -> None:
        self._data = data
        self._next = next

    @property
    def data(self) -> object:
        return self._data
    
    @data.setter
    def data(self, data: object) -> None:
        self._data = data

    @property
    @abstractmethod
    def next(self) -> 'Node':
        ...
    
    @next.setter
    @abstractmethod
    def next(self, next: 'Node') -> None:
        ...


class SingleNode(Node):
    def __init__(self, data: object, next: 'SingleNode' = None) -> None:
        super().__init__(data, next)

    @property
    def next(self) -> 'SingleNode':
        return self._next
    
    @next.setter
    def next(self, next: 'SingleNode') -> None:
        self._next = next


class DoubleNode(Node):
    def __init__(self, data: object, prev: 'DoubleNode' = None, next: 'DoubleNode' = None) -> None:
        super().__init__(data, next)
        self._prev = prev

    @property
    def next(self) -> 'DoubleNode':
        return self._next
    
    @next.setter
    def next(self, next: 'DoubleNode') -> None:
        self._next = next

    @property
    def prev(self) -> 'DoubleNode':
        return self._prev
    
    @prev.setter
    def prev(self, prev: 'DoubleNode') -> None:
        self._prev = prev
