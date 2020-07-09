import classier.decorators.has_state_decorator.options.ATTRIBUTE_OPTIONS as ATTRIBUTE_OPTIONS
import classier.decorators.has_state_decorator.options.MAGIC_METHODS_OPTIONS as MAGIC_METHODS_OPTIONS
import classier.decorators.has_state_decorator.options.METHOD_OPTIONS as METHOD_OPTIONS
from classier.decorators.has_state_decorator._add_state_methods._add_from_pointer import _get_from_pointer
from classier.decorators import _MARK_ATTRIBUTE_NAME
from classier.decorators.has_state_decorator import _MARK_TYPE_NAME
from classier.objects import ClassMarker
import classier.utils as utils
import inspect
import copy


def _add__init__(some_class, options):
    state_attribute_name = ATTRIBUTE_OPTIONS.ATTRIBUTE_NAME_STATE.get_option(options)
    default_state = ATTRIBUTE_OPTIONS.ATTRIBUTE_VALUE_DEFAULT_STATE.get_option(options)
    post_pointer_init = MAGIC_METHODS_OPTIONS.__INIT__METHOD_POST_POINTER_INIT.get_option(options)
    pointer_name = MAGIC_METHODS_OPTIONS.__INIT__ARGUMENT_NAME_POINTER.get_option(options)
    from_pointer_default = METHOD_OPTIONS.METHOD_POINTER_DEFAULT.get_option(options)

    old__init__ = some_class.__init__
    old__init__signature = inspect.signature(old__init__)
    old__init__parameters = old__init__signature.parameters.keys()
    from_pointer = _get_from_pointer(options)

    def new__init__(self, *args, **kwargs):
        pointer = kwargs.get(pointer_name)

        copied_default_state = copy.deepcopy(default_state)
        # pass any other supplementary information to default function if needed
        def default(p):
            val = utils.convenience.call(from_pointer_default,
                                         args=args,
                                         kwargs=kwargs)
            return utils.convenience.set_default(val, copied_default_state)
        if pointer is not None and pointer_name not in old__init__parameters:
            from_pointer(self, pointer, default=default)
            if post_pointer_init is not None:
                utils.convenience.call(post_pointer_init, args=(self, *args), kwargs=kwargs)
        else:
            setattr(self, state_attribute_name, copied_default_state)
            utils.convenience.call(old__init__, args=(self, *args), kwargs=kwargs)

    method_name_init = "__init__"
    if not ClassMarker.does_mark_exist(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_init):
        ClassMarker.add_mark_to_class(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_init)
        some_class = utils.convenience.add_mixin(some_class, new__init__, method_name_init)
    return some_class
