from pytest import fixture
from linkeds import BoundedStack, DynamicStack


PROCESSES = (
    'Kernel', 'Scheduler', 'MemoryManager', 'Filesystem', 'NetworkManager', 'ProcessDispatcher',
    'IOManager', 'SecurityDaemon', 'VirtualMachine', 'DatabaseServer', 'WebServer'
)


@fixture
def bounded_stack() -> BoundedStack:
    stack = BoundedStack(len(PROCESSES))

    for process in PROCESSES:
        stack.push(process)

    return stack


@fixture
def dynamic_stack() -> DynamicStack:
    stack = DynamicStack()

    for process in PROCESSES:
        stack.push(process)

    return stack


def test_bounded_stack(bounded_stack: BoundedStack) -> None:
    assert bounded_stack.is_empty() is False
    assert bounded_stack.is_full() is True

    for i in range(bounded_stack.size):
        assert bounded_stack.peek() == PROCESSES[-(i + 1)]
        assert bounded_stack.pop() == PROCESSES[-(i + 1)]

    assert bounded_stack.is_empty() is True


def test_dynamic_stack(dynamic_stack: DynamicStack) -> None:
    assert dynamic_stack.is_empty() is False

    for i in range(dynamic_stack.size):
        assert dynamic_stack.peek() == PROCESSES[-(i + 1)]
        assert dynamic_stack.pop() == PROCESSES[-(i + 1)]

    assert dynamic_stack.is_empty() is True
