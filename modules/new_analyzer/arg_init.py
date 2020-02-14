def init_arg(arg_name, kwargs):
    if arg_name in kwargs:
        return kwargs[arg_name]
    else:
        print("Error: missing '{}' argument".format(arg_name))
        exit(1)
