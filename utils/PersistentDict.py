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

    def __contains__(self, key):
        return self.contains(key)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.delete(key)

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

    def get(self, key: str, default: object=None, getter=None, decrypt=False):
        val = self.read().get(key, default) if getter is None else getter(key)
        if decrypt:
            assert isinstance(val, str)
            val = self.decrypt(val)
        return val

    def delete(self, key: str) -> dict:
        data = self.read()
        if key in data:
            del data[key]
        self.save(data)
        return data

    def set(self, key: str, val: object, encrypt=False) -> dict:
        data = self.read()
        if encrypt:
            assert isinstance(val, str)
            val = self.encrypt(val)
        data[key] = val
        self.save(data)
        return data

    def contains(self, key: str) -> bool:
        return key in self.read()

    def get_or_ask(self, key: str, ask_fn=lambda: input("String Input:"), getter=None, decrypt=False):
        val = self.get(key, getter=getter, decrypt=decrypt)
        if val is None:
            print(f"{key} is not found, please enter below.")
            val = ask_fn()
            self.set(key, val, encrypt=decrypt)
        return val

    def erase_file(self, ask_for_confirmation=True):
        cmd = f"rm {self.file}"
        if ask_for_confirmation:
            if not get_yes_no(f'This is going to execute {cmd}, are you sure?'):
                print("Aborted")
        subprocess.call(cmd.split(" "))

    @staticmethod
    def encrypt(val):
        return base64.b64encode(val.encode("utf-8")).decode()

    @staticmethod
    def decrypt(val):
        return base64.b64decode(val.encode().decode("utf-8")).decode()
