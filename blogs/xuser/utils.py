def handle_serializer_errors(serializer_error):

    error_keys = [keyy for keyy in serializer_error.keys()]
    message = f"{error_keys[0]}: {serializer_error[error_keys[0]][0]}"
    return message