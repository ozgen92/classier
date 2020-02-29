
def _add__getitem__(some_class, state_attribute_name):
    def new__getitem__(self, key):
        state = getattr(self, state_attribute_name)
        return state.get(key)
    some_class.__getitem__ = new__getitem__
