import classier.utils.convenience as convenience
import classier.locks as locks
import subprocess
import json
import os

"""
Below sets the attributes classier will use.
Rename them as you wish, however they need to be valid strings
"""

ATTRIBUTE_NAME_STATE = "state"  # classier will use this attribute to handle state related behavior
ATTRIBUTE_VALUE_DEFAULT_STATE = {}  # each state will be initialized to a copy of this dictionary
ATTRIBUTE_NAME_STATE_POINTER = "_state_file"  # this holds where the state is saved, for deleting purposes


def WRITE_STATE(self: dict, state_pointer: str):
    """defines how state is saved"""
    with locks.WriteLock(state_pointer), open(state_pointer, "w") as f:
        json.dump(_GET_STATE(self), f, ensure_ascii=False, indent=4, sort_keys=True, default=lambda o: str(o))


def READ_STATE(state_pointer: str) -> dict:
    """defines how state is read"""
    with locks.ReadLock(state_pointer), open(state_pointer, "r") as f:
        return json.loads(f.read())


def DELETE_STATE(state_pointer: str):
    """defines how state is deleted"""
    if state_pointer is not None and os.path.exists(state_pointer):
        subprocess.call(["rm", state_pointer])
        current_dir = os.path.dirname(state_pointer)
        while current_dir != "./" and len(os.listdir(current_dir)) == 0 and os.path.exists(current_dir):
            subprocess.call(["rm", "-r", current_dir])
            current_dir = os.path.dirname(current_dir)


def GET_STATE_POINTER(self):
    """defines how the state_pointer is generated"""
    from classier.decorators.has_state_decorator.options.INDEX_OPTIONS import INDEX_POINTER
    dir = os.path.dirname(INDEX_POINTER)  # just write to wherever the index is saved by default
    return os.path.join(dir, "state.json")


def _GET_STATE(self):
    return getattr(self, ATTRIBUTE_NAME_STATE)

