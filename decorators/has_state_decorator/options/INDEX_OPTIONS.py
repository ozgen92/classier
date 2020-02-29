import classier.locks as locks
import json


"""
Below is to configure index related behavior
"""

INDEX_POINTER = "./states/index.json"  # Set to None if you dont want to use indexing
GET_ID = None  # A function that takes an instance of the class and returns an unique string identifier for indexing


def WRITE_INDEX(state: dict, index_pointer: str):
    """an optional function, to replace how index is saved"""
    with locks.WriteLock(index_pointer), open(index_pointer, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=4, sort_keys=True, default=lambda o: str(o))


def READ_INDEX(index_pointer: str) -> dict:
    """an optional function, to replace how index is read"""
    with locks.ReadLock(index_pointer), open(index_pointer, "r") as f:
        return json.loads(f.read())

