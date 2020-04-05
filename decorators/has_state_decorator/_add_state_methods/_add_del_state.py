import classier.decorators.has_state_decorator.options.ATTRIBUTE_OPTIONS as ATTRIBUTE_OPTIONS
import classier.decorators.has_state_decorator.options.METHOD_OPTIONS as METHOD_OPTIONS
from classier.decorators import _MARK_ATTRIBUTE_NAME
from classier.decorators.has_state_decorator import _MARK_TYPE_NAME
from classier.objects import ClassMarker
import classier.utils as utils


def _add_del_state(some_class, options):
    state_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE.get_option(options)
    state_pointer_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE_POINTER.get_option(options)

    get_id = METHOD_OPTIONS.METHOD_GET_ID.get_option(options)
    saver = METHOD_OPTIONS.METHOD_SAVER.get_option(options)
    index = METHOD_OPTIONS.METHOD_INDEX.get_option(options)
    index_path = METHOD_OPTIONS.PATH_INDEX.get_option(options)

    def del_state(self, remove_empty_directories=True):
        state = getattr(self, state_attribute_name)
        state_pointer = state.get(state_pointer_attribute_name)
        if state_pointer is not None:
            state_id = None if get_id is None else str(get_id(self))
            index_information = None
            if index is not None and state_id is not None:
                index_information = index(state_id, type(self), index_path)
            saver.delete(state_pointer, index_information=index_information, remove_empty_directories=remove_empty_directories)

    method_name_del = METHOD_OPTIONS.METHOD_NAME_DEL_STATE.get_option(options)
    if not ClassMarker.does_mark_exist(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_del):
        ClassMarker.add_mark_to_class(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_del)
        some_class = utils.convenience.add_mixin(some_class, del_state, method_name_del)
    return some_class
