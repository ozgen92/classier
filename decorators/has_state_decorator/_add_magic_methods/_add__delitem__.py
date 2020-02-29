
def _add__delitem__(some_class, state_attribute_name):
    def new__delitem__(self, key):
        state = getattr(self, state_attribute_name)
        if key in state:
            del state[key]
    some_class.__delitem__ = new__delitem__
