import classier.decorators.has_state_decorator.options.ATTRIBUTE_OPTIONS as ATTRIBUTE_OPTIONS
import classier.decorators.has_state_decorator.options.METHOD_OPTIONS as METHOD_OPTIONS
from classier.objects import ClassMarker
from classier.decorators import _MARK_ATTRIBUTE_NAME
from classier.decorators.has_state_decorator import _MARK_TYPE_NAME
import classier.utils as utils


def _add_get_state_path(some_class, options):
    state_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE.get_option(options)
    state_pointer_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE_POINTER.get_option(options)

    def get_state_path(self):
        state = getattr(self, state_attribute_name)
        return state.get(state_pointer_attribute_name)

    method_name_get_state_path = METHOD_OPTIONS.METHOD_NAME_GET_STATE_PATH.get_option(options)
    if not ClassMarker.does_mark_exist(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_get_state_path):
        ClassMarker.add_mark_to_class(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_get_state_path)
        some_class = utils.convenience.add_mixin(some_class, get_state_path, method_name_get_state_path)
    return some_class
