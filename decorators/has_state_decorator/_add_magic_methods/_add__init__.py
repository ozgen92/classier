import classier.decorators.has_state_decorator.options.ATTRIBUTE_OPTIONS as ATTRIBUTE_OPTIONS
from classier.decorators.has_state_decorator._add_state_methods._add_from_pointer import _get_from_pointer
from classier.decorators import _MARK_ATTRIBUTE_NAME
from classier.decorators.has_state_decorator import _MARK_TYPE_NAME
from classier.objects import ClassMarker
import classier.utils as utils
import copy


def _add__init__(some_class, options):
    state_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE.get_option(options)
    default_state = ATTRIBUTE_OPTIONS.ATTRIBUTE_VALUE_DEFAULT_STATE.get_option(options)

    old__init__ = some_class.__init__
    from_pointer = _get_from_pointer(options)

    def new__init__(self, *args, **kwargs):
        pointer = kwargs.get("pointer")
        # if pointer is None and len(args) == 1 and (isinstance(pointer, str) or isinstance(pointer, dict)):
        #     pointer = args[0]

        copied_default_state = copy.deepcopy(default_state)
        if pointer is not None:
            from_pointer(self, pointer, default=lambda p: copied_default_state)
        else:
            setattr(self, state_attribute_name, copied_default_state)
            utils.convenience.call(old__init__, args=(self, *args), kwargs=kwargs)

    method_name_init = "__init__"
    if not ClassMarker.does_mark_exist(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_init):
        ClassMarker.add_mark_to_class(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_init)
        some_class = utils.convenience.add_mixin(some_class, new__init__, method_name_init)
    return some_class
