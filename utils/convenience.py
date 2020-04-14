import inspect


def set_default(val, default, when=None):
    if when is None and val is when or val == when:
        return default
    else:
        return val


def optional(some_fn, default=None):
    try:
        return some_fn()
    except:
        return default


def add_mixin(some_class, some_fn, fn_name):
    new_class = type(some_class.__name__, (some_class,), {
        fn_name: some_fn
    })
    return new_class


def call(fn, args=None, kwargs=None):
    args = set_default(args, tuple())
    kwargs = set_default(kwargs, dict())

    signature = inspect.signature(fn)
    parameters = signature.parameters
    args_index = 0
    to_pass = {}
    for expected_arg in parameters.keys():
        if expected_arg in kwargs.keys():
            to_pass[expected_arg] = kwargs[expected_arg]
        else:
            to_pass[expected_arg] = args[args_index]
            args_index += 1
        if args_index == len(args):
            break
    fn(**to_pass)
