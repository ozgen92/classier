from abc import ABCMeta, abstractmethod


class AbstractSaver(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def save(file, path, index_information=None):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get(file_pointer, index_information=None):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def delete(file_pointer, index_information=None):
        raise NotImplementedError
