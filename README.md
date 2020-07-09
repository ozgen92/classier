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
 
#### @has_state
 - easy way to save, index and retrieve object states if you are dealing with many instances
 
```
from classier.decorators.has_state_decorator.has_state import has_state
from classier.decorators.has_state_decorator.options.METHOD_OPTIONS import METHOD_GET_ID
@has_state({METHOD_GET_ID.name: lambda x: x.state['id']})
class a:
    def __init__(self, some_id):
        print(id(self))
        self.state["id"] = some_id
x1 = a(12)
x2 = a(14)
x1["x","y"] = 1
x1.save_state()
x2.save_state()
print(f"{str(x1)}, {len(x1)}")
x1 = a(pointer=x1["_state_file"])
del x1["x"]
print(f"{x1.get_state()}, {len(x1)}")
x1.delete_state()
x2.delete_state()
```
