import json


def _add__str__(some_class, state_attribute_name):
    def new__str__(self):
        state = getattr(self, state_attribute_name)
        return json.dumps(state, default=lambda o: str(o), ensure_ascii=False, indent=4, sort_keys=True)
    some_class.__str__ = new__str__
