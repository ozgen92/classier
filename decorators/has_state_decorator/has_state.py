from classier.decorators.has_state_decorator.options import get_full_options
import classier.utils.convenience as convenience
import classier.locks as locks
import subprocess
import json
import os

# TODO: class wide cached index so you dont have to keep reading/writing that over and over
# would need a class function that would be executed periodically and before python exits

# a similar problem: different methods of the same function are calculating the same variable over and over again
# you dont want to bother passing that around but you also dont want to waste your time.
# use memoized functions (cache size could be as low as 1)

# use persistent dict instead of index
# use memoization & lazyness on persistent dict
# make idempotent (if already existing, dont update, by marking _classier_decorations)


# Name defaults
NAMING = "naming"
METHOD_NAME_SAVE_STATE = "save_state"
METHOD_NAME_GET_STATE = "get_state"
METHOD_NAME_DEL_STATE = "del_state"
METHOD_NAME_FROM_POINTER = "from"
METHOD_NAME_GET_ID = "get_id"
STATE_ATTRIBUTE_NAME = "state"


# Option defaults
OPTION_WITH__STR__ = "with__str__"
OPTION_WITH__SETITEM__ = "with__setitem__"
OPTION_WITH__GETITEM__ = "with__getitem__"
OPTION_WITH__DELITEM__ = "with__delitem__"
DEFAULT_STATE = {}

# Finding information about saving
INDEX_FILE_PATH = "index_file_path"
STATE_FILE_ATTRIBUTE_NAME = "_state_path"
FILE_TO_STATE = "file_to_state"
ID_GETTER = "id_getter"
PATH_GETTER = "path_getter"

def has_state(options=None):
    """
    :param options: a subset of DEFAULT_OPTIONS to customize the behavior
    :return: returns a decorator that equips classes with some convenience methods to save, delete, modify state
    """
    options = convenience.set_default(options, DEFAULT_OPTIONS)
    naming = options.get(NAMING, DEFAULT_OPTIONS[NAMING])
    method_name_save = naming.get(METHOD_NAME_SAVE_STATE, DEFAULT_OPTIONS[METHOD_NAME_SAVE_STATE])
    method_name_get_state = naming.get(METHOD_NAME_GET_STATE, DEFAULT_OPTIONS[METHOD_NAME_GET_STATE])
    method_name_del = naming.get(METHOD_NAME_DEL_STATE, DEFAULT_OPTIONS[METHOD_NAME_DEL_STATE])
    method_name_from = naming.get(METHOD_NAME_FROM_POINTER, DEFAULT_OPTIONS[METHOD_NAME_FROM_POINTER])
    method_name_get_id = naming.get(METHOD_NAME_GET_ID, DEFAULT_OPTIONS[METHOD_NAME_GET_ID])
    state_attribute_name = naming.get(STATE_ATTRIBUTE_NAME, DEFAULT_OPTIONS[STATE_ATTRIBUTE_NAME])
    state_file_attribute_name = naming.get(STATE_FILE_ATTRIBUTE_NAME, DEFAULT_OPTIONS[STATE_FILE_ATTRIBUTE_NAME])

    option_with_str = options.get(OPTION_WITH__STR__, DEFAULT_OPTIONS[OPTION_WITH__STR__])
    option_with_setitem = options.get(OPTION_WITH__SETITEM__, DEFAULT_OPTIONS[OPTION_WITH__SETITEM__])
    option_with_getitem = options.get(OPTION_WITH__GETITEM__, DEFAULT_OPTIONS[OPTION_WITH__GETITEM__])
    option_with_delitem = options.get(OPTION_WITH__DELITEM__, DEFAULT_OPTIONS[OPTION_WITH__DELITEM__])
    default_state = options.get(DEFAULT_STATE, DEFAULT_OPTIONS[DEFAULT_STATE])

    file_to_state = options.get(FILE_TO_STATE, DEFAULT_OPTIONS[FILE_TO_STATE])
    path_getter = options.get(PATH_GETTER, DEFAULT_OPTIONS[PATH_GETTER])
    id_getter = options.get(ID_GETTER, DEFAULT_OPTIONS[ID_GETTER])
    index_file_path = options.get(INDEX_FILE_PATH, DEFAULT_OPTIONS[INDEX_FILE_PATH])

    def customized_has_state_decorator(some_class):
        """
        :param some_class: this is a decorator, so it takes a class as an argument
        :return: returns the class equipped with some convenience methods to save, delete, modify state
        """
        # TODO: organize by context and comment
        def read_state_from_file(state_file):
            with locks.ReadLock(state_file), open(state_file, "r") as f:
                return json.loads(f.read())

        def get_state_file(self):
            state_file_name = "state"
            if id_getter is not None:
                self_id = id_getter(self)
                state_file_name = f"{state_file_name}_{self_id}"
            return state_file_name

        def get_index():
            if index_file_path is None or not os.path.exists(index_file_path):
                return None
            with locks.ReadLock(index_file_path), open(index_file_path, "r") as f:
                return json.loads(f.read())

        def has_indexed_state(self):
            return get_state_from_index(self) is not None

        def get_state_from_index(self):
            if id_getter is None:
                return False
            self_id = id_getter(self)
            index = get_index()
            if index is None:
                return False
            index_of_class = index.get(self.__name__)
            if index_of_class is None:
                return False
            return index_of_class.get(self_id)

        def index_state(self):
            if id_getter is None:
                return
            self_id = id_getter(self)
            index = get_index()
            if index is None:
                return

            if self.__name__ not in index:
                index[self.__name__] = {}
            state_file_name = get_state_file(self)
            index[self.__name__][self_id] = state_file_name
            with locks.WriteLock(index_file_path), open(index_file_path, "w") as f:
                json.dump(index, f, ensure_ascii=False, indent=4, sort_keys=True, default=lambda o: str(o))

        if method_name_save is not None:
            def save(self, state_path):
                state = getattr(self, state_attribute_name)
                state[state_file_attribute_name] = state_path
                if not os.path.exists(state_path):
                    os.makedirs(state_path, exist_ok=True)
                index_state(self)

                state_file_name = get_state_file(self)
                state_file = os.path.join(state_path, state_file_name)
                with locks.WriteLock(state_file), open(state_file, "w") as f:
                    state = getattr(self, state_attribute_name)
                    json.dump(state, f, ensure_ascii=False, indent=4, sort_keys=True, default=lambda o: str(o))
            if path_getter is not None:
                def save_state(self):
                    state_path = path_getter(self)
                    save(self, state_path)
            else:
                def save_state(self, path="./"):
                    save(self, path)
            setattr(some_class, method_name_save, save_state)

        if method_name_get_state is not None:
            def get_state(self):
                return getattr(self, state_attribute_name)
            setattr(some_class, method_name_get_state, get_state)

        if method_name_del is not None:
            def del_state(self):
                if state_file_attribute_name in self.__dict__:
                    state = getattr(self, state_attribute_name)
                    state_file = state.get(state_file_attribute_name)
                    if state_file is not None and os.path.exists(state_file):
                        subprocess.call(["rm", state_file])
                        current_dir = os.path.dirname(state_file)
                        while current_dir != "./" and len(os.listdir(current_dir)) == 0 and os.path.exists(current_dir):
                            subprocess.call(["rm", "-r", current_dir])
                            current_dir = os.path.dirname(current_dir)
            setattr(some_class, method_name_del, del_state)

        if method_name_get_id is not None and id_getter is not None:
            setattr(some_class, method_name_get_id, id_getter)

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

        if option_with_str:
            def new__str__(self):
                state = getattr(self, state_attribute_name)
                return json.dumps(state, default=lambda o: str(o), ensure_ascii=False, indent=4, sort_keys=True)
            some_class.__str__ = new__str__

        if option_with_setitem:
            def new__setitem__(self, key, val):
                state = getattr(self, state_attribute_name)
                state[key] = val
            some_class.__setitem__ = new__setitem__

        if option_with_getitem:
            def new__getitem__(self, key):
                state = getattr(self, state_attribute_name)
                return state.get(key)
            some_class.__getitem__ = new__getitem__

        if option_with_delitem:
            def new__delitem__(self, key):
                state = getattr(self, state_attribute_name)
                if key in state:
                    del state[key]
            some_class.__delitem__ = new__delitem__

        return some_class

    return customized_has_state_decorator


DEFAULT_OPTIONS = {
    NAMING: {
        METHOD_NAME_SAVE_STATE: METHOD_NAME_SAVE_STATE,
        METHOD_NAME_GET_STATE: METHOD_NAME_GET_STATE,
        METHOD_NAME_DEL_STATE: METHOD_NAME_DEL_STATE,
        METHOD_NAME_FROM_POINTER: METHOD_NAME_FROM_POINTER,
        METHOD_NAME_GET_ID: METHOD_NAME_GET_ID,
        STATE_ATTRIBUTE_NAME: STATE_ATTRIBUTE_NAME,
        STATE_FILE_ATTRIBUTE_NAME: STATE_FILE_ATTRIBUTE_NAME
    },
    OPTION_WITH__STR__: True,
    OPTION_WITH__SETITEM__: True,
    OPTION_WITH__GETITEM__: True,
    OPTION_WITH__DELITEM__: True,
    "DEFAULT_STATE": {},
    FILE_TO_STATE: None,  # a function that takes a dictionary read from a file, and converts it to a valid state
    PATH_GETTER: None,  # a function that takes an instance of the class and returns a path to save
    ID_GETTER: None,  # a function that takes an instance of the class and returns an unique identifier
    INDEX_FILE_PATH: "./states/index.json"  # can be None
}


def _GET_OPTIONS(options: dict) -> dict:
    for var_name, var_val in locals():
        if not var_name.startswith("_"):
            options[var_name] = convenience.set_default(options.get(var_name), var_val)
    return options
