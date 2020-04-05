import classier.decorators.has_state_decorator.options.ATTRIBUTE_OPTIONS as ATTRIBUTE_OPTIONS
import classier.decorators.has_state_decorator.options.METHOD_OPTIONS as METHOD_OPTIONS
from classier.decorators import _MARK_ATTRIBUTE_NAME
from classier.decorators.has_state_decorator import _MARK_TYPE_NAME
from classier.objects import ClassMarker
import classier.utils as utils
import os


def _add_save_state(some_class, options):
    state_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE.get_option(options)
    state_pointer_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE_POINTER.get_option(options)

    get_id = METHOD_OPTIONS.METHOD_GET_ID.get_option(options)
    saver = METHOD_OPTIONS.METHOD_SAVER.get_option(options)
    index = METHOD_OPTIONS.METHOD_INDEX.get_option(options)
    index_path = METHOD_OPTIONS.PATH_INDEX.get_option(options)

    def save_state(self, file_path=None):
        state = getattr(self, state_attribute_name)
        state_id = None if get_id is None else str(get_id(self))

        if file_path is None:
            get_path = METHOD_OPTIONS.METHOD_GET_PATH.get_option(options)
            path = get_path(self)
            assert state_id is not None
            file_path = os.path.join(path, state_id)

        index_information = None
        if index is not None and state_id is not None:
            index_information = index(state_id, type(self), index_path)
        state[state_pointer_attribute_name] = file_path
        saver.save(state, file_path, index_information)

    method_name_save_state = METHOD_OPTIONS.METHOD_NAME_SAVE_STATE.get_option(options)
    if not ClassMarker.does_mark_exist(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_save_state):
        ClassMarker.add_mark_to_class(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_save_state)
        some_class = utils.convenience.add_mixin(some_class, save_state, method_name_save_state)
    return some_class
