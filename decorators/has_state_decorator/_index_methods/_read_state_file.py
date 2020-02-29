import classier.locks as locks
import json


def read_state_file(state_file):
    with locks.ReadLock(state_file), open(state_file, "r") as f:
        return json.loads(f.read())
