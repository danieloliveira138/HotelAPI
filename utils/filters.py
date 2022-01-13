def normalize_dictionary(args):
    return {key: args[key] for key in args if args[key] is not None}
