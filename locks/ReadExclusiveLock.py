import classier.locks as locks


class ReadExclusiveLock(locks.AbstractLock):
    def __enter__(self):
        locks._name_space.wait_and_acquire(self.name,
                                           [locks.ReadExclusiveLock],
                                           [locks.ReadExclusiveLock, locks.WriteLock],
                                           self.thread_id)
