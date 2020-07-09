import datetime
import inspect

def set_default(val, default, when=None):
    if when is None:
        if val is None:
            return default
        else:
            return val
    else:
        if when(val):
            return default
        else:
            return val


def parse_timestamp(time):
    if isinstance(time, datetime.datetime):
        return time
    formats_to_try = [
        "%Y-%m-%dT%H:%M:%S.%f+00:00",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S,%f",
        "%d-%m-%Y",
    ]
    for format in formats_to_try:
        try:
            return datetime.datetime.strptime(time, format)
        except:
            pass

    try:
        return datetime.datetime.utcfromtimestamp(int(time)/1000)
    except:
        pass

    raise ValueError(f"Unrecognized format {time}")


def round_date(date, round_up=False):
    rounded = datetime.datetime.strptime(date.strftime("%d-%m-%Y"), "%d-%m-%Y")
    if round_up:
        rounded = rounded + datetime.timedelta(days=1)
    return rounded


convert_seconds_to = {
    "us": 10**6,
    "ms": 10**3,
    "s": 1,
    "m": 1/60,
    "h": 1/3600,
}

def optional(some_fn, default=None):
    try:
        return some_fn()
    except:
        return default


def add_mixin(some_class, some_fn, fn_name):
    if hasattr(some_class, fn_name) and not (fn_name.startswith("__") and fn_name.endswith("__")):
        raise AttributeError(f"{some_class.__name__} already has {fn_name} implemented!")
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

    # first pass kwargs
    for expected_arg in parameters.keys():
        if expected_arg in kwargs.keys():
            to_pass[expected_arg] = kwargs[expected_arg]

    # then start passing arguments one by one in order
    for expected_arg in parameters.keys():
        # first check if argument is already passed
        if expected_arg in to_pass.keys():
            continue
        if len(args) > args_index:
            to_pass[expected_arg] = args[args_index]
            args_index += 1
        if args_index == len(args):
            break
    return fn(**to_pass)
