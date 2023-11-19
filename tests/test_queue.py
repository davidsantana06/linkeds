from pytest import fixture
from src.data_structures import BoundedQueue, DynamicQueue


COMPONENTS = (
    'Processor', 'Memory', 'Storage', 'OperatingSystem', 'NetworkInterface', 'Database',
    'WebBrowser', 'Firewall', 'Compiler', 'Router', 'WebServer', 'GraphicsCard', 'BluetoothModule', 
    'PeripheralDevices', 'API', 'LoadBalancer', 'DNS', 'VersionControlSystem', 'EncryptionModule', 
    'AuthenticationService', 'BackupSystem', 'VirtualizationPlatform'
)


@fixture
def bounded_queue() -> BoundedQueue:
    queue = BoundedQueue(len(COMPONENTS))

    for component in COMPONENTS:
        queue.enqueue(component)

    return queue


@fixture
def dynamic_queue() -> DynamicQueue:
    queue = DynamicQueue()

    for component in COMPONENTS:
        queue.enqueue(component)

    return queue


def test_bounded_queue(bounded_queue: BoundedQueue) -> None:
    assert bounded_queue.is_empty() is False
    assert bounded_queue.is_full() is True

    for i in range(bounded_queue.size):
        assert bounded_queue.peek() == COMPONENTS[i]
        assert bounded_queue.dequeue() == COMPONENTS[i]

    assert bounded_queue.is_empty() is True


def test_dynamic_queue(dynamic_queue: DynamicQueue) -> None:
    assert dynamic_queue.is_empty() is False

    for i in range(dynamic_queue.size):
        assert dynamic_queue.peek() == COMPONENTS[i]
        assert dynamic_queue.dequeue() == COMPONENTS[i]

    assert dynamic_queue.is_empty() is True
