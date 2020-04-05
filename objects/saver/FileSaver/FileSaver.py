from classier.objects.saver.AbstractSaver import AbstractSaver
import classier.locks as locks
import subprocess
import json
import os


class FileSaver(AbstractSaver):

    @staticmethod
    def save(data, file_path, index_information=None):
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name, exist_ok=True)

        with locks.WriteLock(file_path), open(file_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, default=lambda o: str(o))

        if index_information is not None:
            index_information.add(file_path)

    @staticmethod
    def get(file_pointer, index_information=None):
        file_pointer, indexed = FileSaver._get_path(file_pointer, index_information)
        if file_pointer is None or not os.path.exists(file_pointer):
            return None

        with locks.ReadLock(file_pointer), open(file_pointer, "r") as f:
            return json.loads(f.read())

    @staticmethod
    def delete(file_pointer, index_information=None, remove_empty_directories=True):
        file_pointer, indexed = FileSaver._get_path(file_pointer, index_information)
        if os.path.exists(file_pointer):
            subprocess.call(["rm", file_pointer])
            if remove_empty_directories:
                current_dir = os.path.dirname(file_pointer)
                while current_dir != os.getcwd() and len(os.listdir(current_dir)) == 0 and os.path.exists(current_dir):
                    subprocess.call(["rm", "-r", current_dir])
                    current_dir = os.path.dirname(current_dir)
        if indexed is not None:
            index_information.remove()

    @staticmethod
    def _get_path(file_pointer, index_information):
        indexed = None
        if index_information is not None:
            indexed = index_information.get()

        no_file_pointer = file_pointer is None or not os.path.exists(file_pointer)
        valid_index = indexed is not None and os.path.exists(indexed)
        if no_file_pointer and valid_index:
            file_pointer = indexed
        return file_pointer, indexed
