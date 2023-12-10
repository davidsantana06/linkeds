from abc import ABC, abstractmethod


class Node(ABC):
    '''Abstract base class for a node.'''

    def __init__(self, data: object, next: 'Node' = None) -> None:
        '''Initializes a Node with the given data and optional reference to the next node.'''
        self._data = data
        self._next = next

    @property
    def data(self) -> object:
        '''Getter method for the data attribute.'''
        return self._data
    
    @data.setter
    def data(self, data: object) -> None:
        '''Setter method for updating the data attribute.'''
        self._data = data

    @property
    @abstractmethod
    def next(self) -> 'Node':
        '''Abstract property for the reference to the next node.'''
        ...

    @next.setter
    @abstractmethod
    def next(self, next: 'Node') -> None:
        '''Abstract setter for updating the reference to the next node.'''
        ...


class SingleNode(Node):
    '''Class representing a single node.'''

    def __init__(self, data: object, next: 'SingleNode' = None) -> None:
        '''Initializes a SingleNode with the given data and optional reference to the next SingleNode.'''
        super().__init__(data, next)

    @property
    def next(self) -> 'SingleNode':
        '''Getter method for the reference to the next SingleNode.'''
        return self._next
    
    @next.setter
    def next(self, next: 'SingleNode') -> None:
        '''Setter method for updating the reference to the next SingleNode.'''
        self._next = next


class DoubleNode(Node):
    '''Class representing a double node.'''

    def __init__(self, data: object, prev: 'DoubleNode' = None, next: 'DoubleNode' = None) -> None:
        '''
        Initializes a DoubleNode with the given data, optional reference to the previous DoubleNode,
        and optional reference to the next DoubleNode.
        '''
        super().__init__(data, next)
        self._prev = prev

    @property
    def next(self) -> 'DoubleNode':
        '''Getter method for the reference to the next DoubleNode.'''
        return self._next
    
    @next.setter
    def next(self, next: 'DoubleNode') -> None:
        '''Setter method for updating the reference to the next DoubleNode.'''
        self._next = next

    @property
    def prev(self) -> 'DoubleNode':
        '''Getter method for the reference to the previous DoubleNode.'''
        return self._prev
    
    @prev.setter
    def prev(self, prev: 'DoubleNode') -> None:
        '''Setter method for updating the reference to the previous DoubleNode.'''
        self._prev = prev
