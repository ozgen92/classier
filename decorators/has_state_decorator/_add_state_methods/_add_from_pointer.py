from classier.decorators.has_state_decorator.options import ATTRIBUTE_OPTIONS
from classier.decorators.has_state_decorator.options import METHOD_OPTIONS
from classier.objects import ClassMarker
from classier.decorators import _MARK_ATTRIBUTE_NAME
from classier.decorators.has_state_decorator import _MARK_TYPE_NAME
import classier.utils as utils


def _get_from_pointer(options):
    pointer_to_state = METHOD_OPTIONS.METHOD_POINTER_TO_STATE.get_option(options)
    pointer_exists = METHOD_OPTIONS.METHOD_POINTER_EXISTS.get_option(options)
    saver = METHOD_OPTIONS.METHOD_SAVER.get_option(options)

    state_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE.get_option(options)

    saver = METHOD_OPTIONS.METHOD_SAVER.get_option(options)
    index = METHOD_OPTIONS.METHOD_INDEX.get_option(options)
    index_path = METHOD_OPTIONS.PATH_INDEX.get_option(options)
    from_pointer_default = METHOD_OPTIONS.METHOD_POINTER_DEFAULT.get_option(options)

    def from_pointer(self, pointer, default=None):
        setattr(self, state_attribute_name, None)
        default = utils.convenience.set_default(default, from_pointer_default)

        index_information = None
        if index is not None:
            index_information = index(pointer, type(self), index_path)

        if isinstance(pointer, dict):
            setattr(self, state_attribute_name, pointer)
        elif isinstance(pointer, str) and pointer_exists(pointer):
            if pointer_to_state is not None:
                state = pointer_to_state(pointer)
            else:
                state = saver.get(pointer, index_information)
            setattr(self, state_attribute_name, state)

        if getattr(self, state_attribute_name, None) is None and default is not None:
            setattr(self, state_attribute_name, default(pointer))

        if getattr(self, state_attribute_name, None) is None:
            raise ValueError(f"Could not initialize from {pointer} of type {type(pointer)}")

        return self
    return from_pointer


def _add_from_pointer(some_class, options):
    method_name_from_pointer = METHOD_OPTIONS.METHOD_NAME_FROM_POINTER.get_option(options)
    if not ClassMarker.does_mark_exist(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_from_pointer):
        ClassMarker.add_mark_to_class(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_from_pointer)
        some_class = utils.convenience.add_mixin(some_class, _get_from_pointer(options), method_name_from_pointer)
    return some_class
