from classier.objects.Option import Option


"""
Below is to enable/disbale setting some magic methods automatically.
Set to True/False only
"""

OPTION_WITH__STR__ = Option("OPTION_WITH__STR__", True)
OPTION_WITH__LEN__ = Option("OPTION_WITH__LEN__", True)
OPTION_WITH__EQ__ = Option("OPTION_WITH__EQ__", True)
OPTION_WITH__INIT__ = Option("OPTION_WITH__INIT__", True)
OPTION_WITH__SETITEM__ = Option("OPTION_WITH__SETITEM__", True)
OPTION_WITH__GETITEM__ = Option("OPTION_WITH__GETITEM__", True)
OPTION_WITH__DELITEM__ = Option("OPTION_WITH__DELITEM__", True)

__INIT__ARGUMENT_NAME_POINTER = Option("__INIT__ARGUMENT_NAME_POINTER", "_pointer")
__INIT__METHOD_POST_POINTER_INIT = Option("__INIT__METHOD_POST_POINTER_INIT", None)  # fn(self, pointer), called after __init__ with_pointer if exists
