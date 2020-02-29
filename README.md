# Classier
This is an experimental package that aims to be as user friendly as possible for generic tasks. 
Bear in mind that it is not thoroughly tested, suggestions & contributions are welcome. 

#### Locks
```
import classier.locks as locks
file_name = "test.txt"

# Concurrent writes to a file (guarantees no other read or write exists or starts)
with locks.WriteLock(file_name), open(file_name, "w") as f:
    f.write("hello!")

# Concurrent reads to a file (guarantees no concurrent write will start)
with locks.ReadLock(file_name), open(file_name, "r") as f:
    print(f.read())

# Exclusive read to a file (guarantees no other read or write will start)
with locks.ReadExclusiveLock(file_name), open(file_name, "r") as f:
    print(f.read())
```


#### PersistentDict

 - Uses a json file on disk as a dictionary.
 - Tolerates concurrent access 
 - Not a good option for speed critical tasks. 

```
from classier import PersistentDict
pd = PersistentDict("test_file")
pd['test_field'] = 'test_value'
# pd.erase_file(ask_for_confirmation=False)
```
 