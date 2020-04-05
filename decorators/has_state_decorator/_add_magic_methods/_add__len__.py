import classier.decorators.has_state_decorator.options.ATTRIBUTE_OPTIONS as ATTRIBUTE_OPTIONS
from classier.decorators import _MARK_ATTRIBUTE_NAME
from classier.decorators.has_state_decorator import _MARK_TYPE_NAME
from classier.objects import ClassMarker
import classier.utils as utils


def _add__len__(some_class, options):
    def new__len__(self):
        state_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE.get_option(options)
        state = getattr(self, state_attribute_name)
        return len(state)

    method_name_len = "__len__"
    if not ClassMarker.does_mark_exist(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_len):
        ClassMarker.add_mark_to_class(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_len)
        some_class = utils.convenience.add_mixin(some_class, new__len__, method_name_len)
    return some_class
