old_init_method = some_class.__init__


def new_init_method(self):
    setattr(self, state_attribute_name, default_state.copy())
    old_init_method(self)


if method_name_from is not None:
    def from_pointer(self, pointer):
        if isinstance(pointer, dict):
            self.state = pointer
        elif isinstance(pointer, str) and os.path.exists(pointer):
            self.state = read_state_from_file(pointer)
            if file_to_state is not None:
                self.state = file_to_state(self.state)
        elif has_indexed_state(self):
            self.state = get_state_from_index(self)
        elif default is not None:
            default(self, pointer)
        else:
            raise ValueError(f"Could not initialize from {pointer} of type {type(pointer)}")
        return self
    setattr(some_class, method_name_from, from_pointer)


    def new_init_method(self, pointer=None):
        setattr(self, state_attribute_name, default_state.copy())
        old_init_method(self)
        if pointer is not None:
            from_pointer(self, pointer)

some_class.__init__ = new_init_method