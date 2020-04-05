import classier.decorators.has_state_decorator.options.ATTRIBUTE_OPTIONS as ATTRIBUTE_OPTIONS
from classier.decorators import _MARK_ATTRIBUTE_NAME
from classier.decorators.has_state_decorator import _MARK_TYPE_NAME
from classier.objects import ClassMarker
import classier.utils as utils


def _add__delitem__(some_class, options):
    def new__delitem__(self, keys):
        if isinstance(keys, str):
            keys = (keys,)
        elif not isinstance(keys, tuple):
            keys = tuple(keys)
        state_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE.get_option(options)
        state = getattr(self, state_attribute_name)
        current = state
        for key in keys[:-1]:
            key = str(key)
            if key not in current:
                return
            current = current[key]

        key = str(keys[-1])
        if key in current:
            del current[key]

    method_name_delitem = "__delitem__"
    if not ClassMarker.does_mark_exist(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_delitem):
        ClassMarker.add_mark_to_class(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_delitem)
        some_class = utils.convenience.add_mixin(some_class, new__delitem__, method_name_delitem)
    return some_class
