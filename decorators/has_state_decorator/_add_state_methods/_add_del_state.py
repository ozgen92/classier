import subprocess
import os


def add_del_state(some_class, method_name_del, state_file_attribute_name, state_attribute_name):
    def del_state(self, remove_empty_directories=True):
        if state_file_attribute_name in self.__dict__:
            state = getattr(self, state_attribute_name)
            state_file = state.get(state_file_attribute_name)
            if state_file is not None and os.path.exists(state_file):
                subprocess.call(["rm", state_file])
                if remove_empty_directories:
                    current_dir = os.path.dirname(state_file)
                    while current_dir != "./" and len(os.listdir(current_dir)) == 0 and os.path.exists(current_dir):
                        subprocess.call(["rm", "-r", current_dir])
                        current_dir = os.path.dirname(current_dir)
    setattr(some_class, method_name_del, del_state)
