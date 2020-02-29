
def add_get_state(some_class, state_attribute_name, method_name_get_state):
    def get_state(self):
        return getattr(self, state_attribute_name)
    setattr(some_class, method_name_get_state, get_state)
