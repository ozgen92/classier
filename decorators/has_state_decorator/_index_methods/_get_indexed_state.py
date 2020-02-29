from classier.decorators.has_state_decorator._index_methods._get_index import get_index


def get_indexed_state(self, id_getter, index_file_path):
    if id_getter is None:
        return False
    self_id = id_getter(self)
    index = get_index(index_file_path)
    if index is None:
        return False
    index_of_class = index.get(self.__name__)
    if index_of_class is None:
        return False
    return index_of_class.get(self_id)
