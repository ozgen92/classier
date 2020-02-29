import classier.locks as locks
import json
import os


def get_index(index_file_path):
    if index_file_path is None or not os.path.exists(index_file_path):
        return None
    with locks.ReadLock(index_file_path), open(index_file_path, "r") as f:
        return json.loads(f.read())
