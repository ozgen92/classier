from classier.decorators.has_state_decorator._add_state_methods._add_from_pointer import _add_from_pointer
from classier.decorators.has_state_decorator._add_state_methods._add_del_state import _add_del_state
from classier.decorators.has_state_decorator._add_state_methods._add_get_state import _add_get_state
from classier.decorators.has_state_decorator._add_state_methods._add_get_state_path import _add_get_state_path
from classier.decorators.has_state_decorator._add_state_methods._add_does_state_exist import add_does_state_exist
from classier.decorators.has_state_decorator._add_state_methods._add_save_state import _add_save_state
from classier.decorators.has_state_decorator._add_state_methods._add_update_state import _add_update_state
from classier.decorators.has_state_decorator.options import METHOD_OPTIONS


def apply(some_class, options):
    if METHOD_OPTIONS.METHOD_NAME_DEL_STATE.get_option(options) is not None:
        some_class = _add_del_state(some_class, options)

    if METHOD_OPTIONS.METHOD_NAME_GET_STATE.get_option(options) is not None:
        some_class = _add_get_state(some_class, options)

    if METHOD_OPTIONS.METHOD_NAME_GET_STATE_PATH.get_option(options) is not None:
        some_class = _add_get_state_path(some_class, options)

    if METHOD_OPTIONS.METHOD_NAME_DOES_STATE_EXIST.get_option(options) is not None:
        some_class = add_does_state_exist(some_class, options)

    if METHOD_OPTIONS.METHOD_NAME_SAVE_STATE.get_option(options) is not None:
        some_class = _add_save_state(some_class, options)

    if METHOD_OPTIONS.METHOD_NAME_UPDATE_STATE.get_option(options) is not None:
        some_class = _add_update_state(some_class, options)

    if METHOD_OPTIONS.METHOD_NAME_FROM_POINTER.get_option(options) is not None:
        some_class = _add_from_pointer(some_class, options)

    get_id = METHOD_OPTIONS.METHOD_GET_ID.get_option(options)
    get_id_method_name = METHOD_OPTIONS.METHOD_NAME_GET_ID.get_option(options)
    if get_id is not None and get_id_method_name is not None:
        setattr(some_class, get_id_method_name, get_id)

    return some_class
