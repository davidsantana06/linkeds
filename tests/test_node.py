from pytest import fixture
from typing import List

from src.data_structures import DoubleNode, SingleNode


NAMES = (
    'Alisson', 'Amanda', 'Camila', 'Gabriel', 'Giovana', 
    'Isabela', 'Kaik', 'Leonardo', 'Lucas', 'Matheus', 'Pedro'
)


@fixture
def single_nodes() -> List[SingleNode]:
    nodes = [SingleNode(NAMES[0])]

    for i, node in enumerate(NAMES[1:], start=1):
        nodes.append(SingleNode(node))
        nodes[i - 1].next = nodes[i]

    return nodes


@fixture
def double_nodes() -> List[DoubleNode]:
    nodes = [DoubleNode(NAMES[0])]

    for i, node in enumerate(NAMES[1:], start=1):
        nodes.append(DoubleNode(node))
        nodes[i - 1].next = nodes[i]
        nodes[i].prev = nodes[i - 1]

    return nodes


def test_single_node(single_nodes: List[SingleNode]) -> None:
    for i, node in enumerate(single_nodes):
        assert node.data == NAMES[i]

        if i < len(single_nodes) - 1:
            assert node.next.data == NAMES[i + 1]


def test_double_node(double_nodes: List[DoubleNode]) -> None:
    for i, node in enumerate(double_nodes):
        assert node.data == NAMES[i]
 
        if i == 0:
            assert node.prev is None
        elif (i > 0) and (i < len(double_nodes) - 1):
            assert node.prev.data == NAMES[i - 1]
            assert node.next.data == NAMES[i + 1]
        else:
            assert node.prev.data == NAMES[i - 1]
            assert node.next is None
