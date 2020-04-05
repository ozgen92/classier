from abc import ABCMeta, abstractmethod


class AbstractIndex(metaclass=ABCMeta):

    def __init__(self, file_id, file_type, index_path):
        self.file_id = file_id
        self.file_type = file_type.__name__
        self.index_path = index_path

    def add(self, path):
        if self._is_valid():
            return self._add(path)

    @abstractmethod
    def _add(self, path):
        raise NotImplementedError

    def get(self):
        if self._is_valid():
            return self._get()

    @abstractmethod
    def _get(self):
        raise NotImplementedError

    def remove(self):
        if self._is_valid():
            return self._remove()

    @abstractmethod
    def _remove(self):
        raise NotImplementedError

    def _is_valid(self):
        return self.file_id is not None and self.file_type is not None and self.index_path is not None
