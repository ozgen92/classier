
def _add__setitem__(some_class, state_attribute_name):
    def new__setitem__(self, key, val):
        state = getattr(self, state_attribute_name)
        state[key] = val
    some_class.__setitem__ = new__setitem__
