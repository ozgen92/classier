from classier.objects.PersistentDict import PersistentDict
from classier.objects.saver import AbstractIndex


class FileIndex(AbstractIndex):
    def __init__(self, file_id, file_type, index_path):
        super().__init__(file_id, file_type, index_path)
        self.index_file = PersistentDict(index_path)

    def _add(self, path):
        self.index_file[self.file_type, self.file_id] = path

    def _get(self):
        return self.index_file[self.file_type, self.file_id]

    def _remove(self):
        del self.index_file[self.file_type, self.file_id]
