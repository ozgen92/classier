import classier.decorators.has_state_decorator._add_magic_methods as _add_magic_methods
import classier.decorators.has_state_decorator._add_state_methods as _add_state_methods
from classier.objects.Option import Option


def has_state(custom_options: dict = None, **kwargs):
    custom_options, input_class = Option.check_callable(custom_options)
    custom_options = Option.with_kwargs(custom_options, kwargs)

    """
    :param custom_options: a dictionary
    :return: returns a decorator that equips classes with defined convenience methods (see sub folders for details)
    """
    def customized_has_state_decorator(some_class):
        """
        :param some_class: this is a decorator, so it takes a class as an argument
        :return: returns the class equipped with some convenience methods to save, delete, modify state
        """
        some_class = _add_magic_methods.apply(some_class, custom_options)
        some_class = _add_state_methods.apply(some_class, custom_options)
        return some_class

    if input_class is not None:
        return customized_has_state_decorator(input_class)

    return customized_has_state_decorator


# TODO: throw exception if a method we are trying to add is already defined