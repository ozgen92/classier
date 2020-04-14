from classier.decorators.has_state_decorator._add_magic_methods._add__delitem__ import _add__delitem__
from classier.decorators.has_state_decorator._add_magic_methods._add__init__ import _add__init__
from classier.decorators.has_state_decorator._add_magic_methods._add__getitem__ import _add__getitem__
from classier.decorators.has_state_decorator._add_magic_methods._add__setitem__ import _add__setitem__
from classier.decorators.has_state_decorator._add_magic_methods._add__str__ import _add__str__
from classier.decorators.has_state_decorator._add_magic_methods._add__len__ import _add__len__
from classier.decorators.has_state_decorator._add_magic_methods._add__eq__ import _add__eq__
from classier.decorators.has_state_decorator.options import MAGIC_METHODS_OPTIONS


def apply(some_class, options):

    if MAGIC_METHODS_OPTIONS.OPTION_WITH__DELITEM__.get_option(options):
        some_class = _add__delitem__(some_class, options)

    if MAGIC_METHODS_OPTIONS.OPTION_WITH__GETITEM__.get_option(options):
        some_class = _add__getitem__(some_class, options)

    if MAGIC_METHODS_OPTIONS.OPTION_WITH__SETITEM__.get_option(options):
        some_class = _add__setitem__(some_class, options)

    if MAGIC_METHODS_OPTIONS.OPTION_WITH__STR__.get_option(options):
        some_class = _add__str__(some_class, options)

    if MAGIC_METHODS_OPTIONS.OPTION_WITH__LEN__.get_option(options):
        some_class = _add__len__(some_class, options)

    if MAGIC_METHODS_OPTIONS.OPTION_WITH__EQ__.get_option(options):
        some_class = _add__eq__(some_class, options)

    if MAGIC_METHODS_OPTIONS.OPTION_WITH__INIT__.get_option(options):
        some_class = _add__init__(some_class, options)
    return some_class
