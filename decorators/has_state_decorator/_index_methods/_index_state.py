from classier.decorators.has_state_decorator._index_methods._get_index import get_index
from classier.decorators.has_state_decorator._index_methods._get_state_file_name import get_state_file_name
import classier.locks as locks
import json


def index_state(self, id_getter, index_file_path):
    if id_getter is None:
        return
    self_id = id_getter(self)
    index = get_index(index_file_path)
    if index is None:
        return

    if self.__name__ not in index:
        index[self.__name__] = {}
    state_file_name = get_state_file_name(self, id_getter)
    index[self.__name__][self_id] = state_file_name
    with locks.WriteLock(index_file_path), open(index_file_path, "w") as f:
        json.dump(index, f, ensure_ascii=False, indent=4, sort_keys=True, default=lambda o: str(o))
