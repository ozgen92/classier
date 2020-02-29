from classier.utils.PersistentDict import PersistentDict
import concurrent.futures
import threading
import subprocess
import os


TEST_FILE = "test_file.json"
if os.path.exists(TEST_FILE):
    subprocess.call(["rm", TEST_FILE])


def write_to_test(val):
    print(f"{threading.get_ident()} is writing {val}")
    PersistentDict(TEST_FILE)['concurrency_test'] = val
    print(f"{threading.get_ident()} is done writing {val}")


with concurrent.futures.ThreadPoolExecutor() as executor:
    tasks = [executor.submit(write_to_test, i) for i in range(1000)]
    results = [task.result() for task in tasks]

with open(TEST_FILE, "r") as f:
    print(f"final value: {f.read()}")
subprocess.call(["rm", TEST_FILE])
