import classier.locks as locks


class WriteLock(locks.AbstractLock):
    def __enter__(self):
        locks._name_space.wait_and_acquire(self.name,
                                           [locks.ReadExclusiveLock],
                                           [locks.ReadExclusiveLock, locks.WriteLock],
                                           self.thread_id)
        locks._name_space.wait_and_acquire(self.name,
                                           [locks.WriteLock],
                                           [locks.ReadLock, locks.ReadExclusiveLock, locks.WriteLock],
                                           self.thread_id)
