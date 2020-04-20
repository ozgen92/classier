class Option:
    """A way to accept flexible number of options from user and to set rest as default"""

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_option(self, options):
        """
        :param options: options can be a list of Option classes or a dictionary
        :return: the opted value or default
        """
        options = self.options_to_names(options)  # in case {Option: value, ...} exist
        if isinstance(options, dict):
            opted_value = options.get(self.name, self)
            if isinstance(opted_value, Option):
                # it is a "name": Option dict
                return opted_value.value
            else:
                # it is a "name": value dict
                return opted_value
        elif isinstance(options, list):
            for option in options:
                if isinstance(option, Option) and option.name == self.name:
                    # it is a list of Option's
                    return option.value
        # if we are here, I dont know what it is, just return the default
        return self.value

    @staticmethod
    def options_to_names(options):
        new_options = {}
        for key, value in options.items():
            if isinstance(key, Option):
                new_options[key.name] = value
            else:
                new_options[key] = value
        return new_options

    @staticmethod
    def with_kwargs(options, kwargs):
        if options is None:
            options = {}
        return {**options, **kwargs}

    @staticmethod
    def check_callable(options):
        if callable(options):
            return {}, options
        else:
            return options, None
