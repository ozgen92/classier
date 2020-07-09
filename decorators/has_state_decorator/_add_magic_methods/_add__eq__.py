import classier.decorators.has_state_decorator.options.METHOD_OPTIONS as METHOD_OPTIONS
from classier.decorators import _MARK_ATTRIBUTE_NAME
from classier.decorators.has_state_decorator import _MARK_TYPE_NAME
from classier.objects import ClassMarker
import classier.utils as utils


def _add__eq__(some_class, options):
    get_id_name = METHOD_OPTIONS.METHOD_NAME_GET_ID.get_option(options)

    def new__eq__(self, other):
        try:
            get_id_self = getattr(self, get_id_name)
            get_id_other = getattr(other, get_id_name)
            return get_id_self() == get_id_other()
        except:
            return False

    method_name_eq = "__eq__"
    if not ClassMarker.does_mark_exist(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_eq):
        ClassMarker.add_mark_to_class(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_eq)
        some_class = utils.convenience.add_mixin(some_class, new__eq__, method_name_eq)
    return some_class
