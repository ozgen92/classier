import classier.locks as locks


class ReadLock(locks.AbstractLock):
    def __enter__(self):
        locks._name_space.wait_and_acquire(self.name,
                                           [locks.ReadLock],
                                           [locks.ReadExclusiveLock, locks.WriteLock],
                                           self.thread_id)
