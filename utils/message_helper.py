def help_message_field_blank(field: str):
    return "The field \'{}\' cannot be left blank".format(field)


def database_unknown_error(name_error: str = None):
    error_complement = name_error if name_error is not None else "An unknown error"
    return {'message': "\'{}\' occurred, please try again.".format(error_complement)}, 500
