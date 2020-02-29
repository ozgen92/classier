import inspect


def set_default(val, default, when=None):
    if when is None and val is when or val == when:
        return default
    else:
        return val


def get_variable_name_as_string(some_variable):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    for var_name, var_val in callers_local_vars:
        if var_val is some_variable:
            return var_name
    return None


def get_full_options(options: dict, local_variables: dict) -> dict:
    """
    :param options: options given by the user
    :param local_variables: locals(), where each capitalized variable is a module containing capitalized variables setting defaults as options
    :return: dictionary filled with default options where appropriate
    """
    for option_type, option_defaults in local_variables:
        if not option_type.isupper():
            continue

        for option_name, option_default in vars(option_defaults):
            if not option_name.isupper():
                continue

            options[option_name] = set_default(options.get(option_name), option_default)

    return options
