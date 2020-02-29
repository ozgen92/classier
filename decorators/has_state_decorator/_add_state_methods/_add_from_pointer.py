from classier.decorators.has_state_decorator._index_methods._read_state_file import read_state_file
from classier.decorators.has_state_decorator._index_methods._get_indexed_state import get_indexed_state
import os


def _get_from_pointer(id_getter, index_file_path,
                      file_to_state=None, default=None):
    def from_pointer(self, pointer):
        if isinstance(pointer, dict):
            self.state = pointer
        elif isinstance(pointer, str) and os.path.exists(pointer):
            self.state = read_state_file(pointer)
            if file_to_state is not None:
                self.state = file_to_state(self.state)
        elif get_indexed_state(self, id_getter, index_file_path) is not None:
            self.state = get_indexed_state(self, id_getter, index_file_path)
        elif default is not None:
            default(self, pointer)
        else:
            raise ValueError(f"Could not initialize from {pointer} of type {type(pointer)}")
        return self
    return from_pointer


def _add_from_pointer(some_class, id_getter, index_file_path,
                      method_name_from_pointer="from_pointer", file_to_state=None, default=None):
    setattr(some_class, method_name_from_pointer, _get_from_pointer(id_getter, index_file_path,
                                                                    file_to_state=file_to_state, default=default))
