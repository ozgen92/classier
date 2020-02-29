import classier.locks as locks
import threading


class LockRecord:
    def __init__(self):
        self._lock_to_owners = {
            # lock_type: {thread_id, ...}
            lock_type: set() for lock_type in (locks.ReadLock, locks.ReadExclusiveLock, locks.WriteLock)
        }
        self.registration_in_progress = threading.Lock()
    
    def attempt_acquire(self, lock_types_to_acquire, lock_types_to_wait, thread_id) -> bool:
        if self.registration_in_progress.locked():
            return False

        try:
            self.registration_in_progress.acquire()
            for lock_type in lock_types_to_wait:
                if self._is_locked(lock_type, thread_id):
                    return False

            for lock_type in lock_types_to_acquire:
                self._acquire(lock_type, thread_id)

            return True
        finally:
            self.registration_in_progress.release()

    def attempt_release_locks(self, thread_id):
        if self.registration_in_progress.locked():
            return False

        try:
            self.registration_in_progress.acquire()
            for lock_type in self._lock_to_owners.keys():
                self._release_lock(lock_type, thread_id)
            return True
        finally:
            self.registration_in_progress.release()

    def _is_locked(self, lock_type, thread_id):
        assert self.registration_in_progress.locked()
        owners = self._lock_to_owners[lock_type]

        if (thread_id in owners and len(owners) == 1) or len(owners) == 0:
            return False
        else:
            return True

    def _acquire(self, lock_type, thread_id):
        assert self.registration_in_progress.locked()
        owners = self._lock_to_owners[lock_type]
        owners.add(thread_id)

    def _release_lock(self, lock_type, thread_id):
        assert self.registration_in_progress.locked()
        owners = self._lock_to_owners[lock_type]
        if thread_id in owners:
            owners.remove(thread_id)
