from classier.decorators.has_state_decorator.options import ATTRIBUTE_OPTIONS
from classier.decorators.has_state_decorator.options import METHOD_OPTIONS
from classier.objects import ClassMarker
from classier.decorators import _MARK_ATTRIBUTE_NAME
from classier.decorators.has_state_decorator import _MARK_TYPE_NAME
import classier.utils as utils
import json


def _get_from_pointer(options):
    state_transformer = METHOD_OPTIONS.METHOD_STATE_TRANSFORMER.get_option(options)
    pointer_exists = METHOD_OPTIONS.METHOD_POINTER_EXISTS.get_option(options)  # TODO: remove?
    saver = METHOD_OPTIONS.METHOD_SAVER.get_option(options)

    state_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE.get_option(options)

    saver = METHOD_OPTIONS.METHOD_SAVER.get_option(options)
    index = METHOD_OPTIONS.METHOD_INDEX.get_option(options)
    index_path = METHOD_OPTIONS.PATH_INDEX.get_option(options)
    from_pointer_default = METHOD_OPTIONS.METHOD_POINTER_DEFAULT.get_option(options)

    def from_pointer(self, pointer, default=None):
        if isinstance(pointer, type(self)):
            setattr(self, state_attribute_name, getattr(pointer, state_attribute_name))
            return pointer

        setattr(self, state_attribute_name, None)
        default = utils.convenience.set_default(default, from_pointer_default)

        index_information = None
        if index is not None:
            index_information = index(pointer, type(self), index_path)

        state = None
        if isinstance(pointer, dict):
            state = pointer
        # TODO: add debug logs here

        if state is None and isinstance(pointer, str):
            # pointer could be json.dumps
            state = utils.convenience.optional(lambda: json.loads(pointer))

        if state is None and isinstance(pointer, str) and index_information is not None:
            # pointer could be something saver knows
            state = utils.convenience.call(lambda: saver.get(pointer, index_information))

        if state is None and default is not None:
            state = default(pointer)

        if state is None:
            raise ValueError(f"Could not initialize from {pointer} of type {type(pointer)}")

        if state_transformer is not None:
            state = state_transformer(state)
        setattr(self, state_attribute_name, state)
        return self
    return from_pointer


def _add_from_pointer(some_class, options):
    method_name_from_pointer = METHOD_OPTIONS.METHOD_NAME_FROM_POINTER.get_option(options)
    if not ClassMarker.does_mark_exist(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_from_pointer):
        ClassMarker.add_mark_to_class(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_from_pointer)
        some_class = utils.convenience.add_mixin(some_class, _get_from_pointer(options), method_name_from_pointer)
    return some_class
