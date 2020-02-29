import classier.locks as locks
import random
import time


class LockNameSpace:

    MIN_WAIT_MS = 2
    MAX_WAIT_MS = 50

    def __init__(self):
        self.lock_names = {
            # some_lock_name: some_lock_record
        }

    def __getitem__(self, lock_name):
        return self._get_lock_record(lock_name)

    def wait_and_acquire(self, lock_name, lock_types_to_acquire, lock_types_to_wait, thread_id):
        lock_record = self._get_lock_record(lock_name)
        while not lock_record.attempt_acquire(lock_types_to_acquire, lock_types_to_wait, thread_id):
            time.sleep(self._get_random_wait_sec())

    def release_locks(self, lock_name, thread_id):
        lock_record = self._get_lock_record(lock_name)
        while not lock_record.attempt_release_locks(thread_id):
            time.sleep(self._get_random_wait_sec())

    def _get_lock_record(self, lock_name):
        if lock_name not in self.lock_names:
            self.lock_names[lock_name] = locks.LockRecord()
        return self.lock_names.get(lock_name)

    def _get_random_wait_sec(self):
        granularity = 10
        return random.randint(self.MIN_WAIT_MS * granularity,
                              self.MAX_WAIT_MS * granularity) / 10**3 / granularity
