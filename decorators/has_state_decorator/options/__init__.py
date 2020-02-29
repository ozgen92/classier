import classier.utils.convenience as convenience
import classier.decorators.has_state_decorator.options.INDEX_OPTIONS as INDEX_OPTIONS
import classier.decorators.has_state_decorator.options.ATTRIBUTE_OPTIONS as ATTRIBUTE_OPTIONS
import classier.decorators.has_state_decorator.options.MAGIC_METHODS_OPTIONS as MAGIC_METHODS_OPTIONS
import classier.decorators.has_state_decorator.options.METHOD_OPTIONS as METHOD_OPTIONS


def get_full_options(options):
    return convenience.get_full_options(options, locals())
