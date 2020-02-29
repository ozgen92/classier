from abc import ABCMeta, abstractmethod
import classier.locks as locks
import threading


# TODO: add timeouts (problem is, a function can timeout without knowing it timed out and attempt to write anyway)


class AbstractLock(metaclass=ABCMeta):

    def __init__(self,
                 name):
        self.name = name
        self.thread_id = threading.get_ident()

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        locks._name_space.release_locks(self.name, self.thread_id)
