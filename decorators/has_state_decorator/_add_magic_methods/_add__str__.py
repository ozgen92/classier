import classier.decorators.has_state_decorator.options.ATTRIBUTE_OPTIONS as ATTRIBUTE_OPTIONS
from classier.decorators import _MARK_ATTRIBUTE_NAME
from classier.decorators.has_state_decorator import _MARK_TYPE_NAME
from classier.objects import ClassMarker
import classier.utils as utils
import json


def _add__str__(some_class, options):
    def new__str__(self):
        state_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE.get_option(options)
        state = getattr(self, state_attribute_name)
        return json.dumps(state, default=lambda o: str(o), ensure_ascii=False, indent=4, sort_keys=True)

    method_name_str = "__str__"
    if not ClassMarker.does_mark_exist(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_str):
        ClassMarker.add_mark_to_class(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_str)
        some_class = utils.convenience.add_mixin(some_class, new__str__, method_name_str)
    return some_class
