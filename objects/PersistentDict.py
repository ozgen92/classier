from classier.utils.input import get_yes_no
import classier.locks as locks
import subprocess
import base64
import json
import os


class PersistentDict:
    def __init__(self, file: str, default=None):
        self.file = file
        if not os.path.exists(file):
            self.save({} if default is None else default)

    def __str__(self):
        return str(self.read())

    def __contains__(self, keys):
        return self.contains(keys)

    def __getitem__(self, items):
        return self.get(items)

    def __setitem__(self, keys, value):
        self.set(keys, value)

    def __delitem__(self, keys):
        self.delete(keys)

    def read(self) -> dict:
        """returns the content of self.file"""
        with locks.ReadLock(self.file), open(self.file, "r") as f:
            return json.loads(f.read())

    def save(self, data: dict) -> None:
        dir_name = os.path.dirname(self.file)
        if dir_name != "":
            os.makedirs(dir_name, exist_ok=True)
        """overwrites self.file with data"""
        with locks.WriteLock(self.file), open(self.file, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

    def get(self, keys, default: object=None, decrypt=False):
        keys, data, current = self._get_subkey(keys, fill_empty=True)
        key = str(keys[-1])
        val = current.get(key, default)
        if decrypt and val is not None:
            assert isinstance(val, str)
            val = self.decrypt(val)
        return val

    def delete(self, keys) -> dict:
        keys, data, current = self._get_subkey(keys, fill_empty=False)
        key = str(keys[-1])

        if current is not None and key in current:
            del current[key]
            self.save(data)
        return data

    def set(self, keys, val, encrypt=False) -> dict:
        keys, data, current = self._get_subkey(keys, fill_empty=True)
        if encrypt:
            assert isinstance(val, str)
            val = self.encrypt(val)

        key = str(keys[-1])
        current[key] = val
        self.save(data)
        return data

    def contains(self, keys) -> bool:
        keys, data, current = self._get_subkey(keys)
        key = str(keys[-1])
        return key in self.read()

    def _get_subkey(self, keys, fill_empty=False):
        data = self.read()
        if isinstance(keys, str):
            keys = (keys,)
        elif not isinstance(keys, tuple):
            keys = tuple(keys)

        current = data
        for i, key in enumerate(keys[0:-1]):
            key = str(key)
            if key not in current:
                if fill_empty:
                    current[key] = {}
                else:
                    return keys, data, None
            current = current[key]
        return keys, data, current

    def get_or_ask(self, keys, ask_fn=lambda: input("String Input:"), decrypt=False):
        val = self.get(keys, decrypt=decrypt)
        if val is None:
            print(f"{keys} is not found, please enter below.")
            val = ask_fn()
            self.set(keys, val, encrypt=decrypt)
        return val

    def erase_file(self, ask_for_confirmation=True):
        cmd = f"rm {self.file}"
        if ask_for_confirmation:
            if not get_yes_no(f"This is going to execute '{cmd}', are you sure?"):
                print("Aborted")
        subprocess.call(cmd.split(" "))

    @staticmethod
    def encrypt(val):
        return base64.b64encode(val.encode("utf-8")).decode()

    @staticmethod
    def decrypt(val):
        return base64.b64decode(val.encode().decode("utf-8")).decode()
