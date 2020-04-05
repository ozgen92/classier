from classier.objects.Option import Option

"""
Below sets the attributes classier will use.
Below can be customized by passing an options dictionary, overwriting the variable
"""

# classier will use this attribute to handle state related behavior
ATTRIBUTE_NAME_STATE = Option("ATTRIBUTE_NAME_STATE", "state")

# each state will be initialized to a copy of this dictionary
ATTRIBUTE_VALUE_DEFAULT_STATE = Option("ATTRIBUTE_VALUE_DEFAULT_STATE", {})

# this holds where the state is saved, for deleting purposes
ATTRIBUTE_NAME_STATE_POINTER = Option("ATTRIBUTE_NAME_STATE_POINTER", "_state_file")
