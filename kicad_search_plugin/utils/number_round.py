def number_round(digit=2):
    def decorate(fn):
        def wrapper(*args, **kwargs):
            return round(fn(*args, **kwargs), digit)

        return wrapper

    return decorate
