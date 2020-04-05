from abc import ABCMeta, abstractmethod
from classier.decorators import has_state


@has_state
class AbstractSandbox(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, cmd):
        # TODO: cmd can be a path of supported file, int pid, a command to be executed
        self.state["cmd"] = cmd
