def help_message_field_blank(field: str):
    return "The field \'{}\' cannot be left blank".format(field)


def database_unknown_error():
    return {'message': 'An error occurred, please try again.'}, 500
