
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
