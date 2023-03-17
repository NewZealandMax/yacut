from random import choice, randrange


def get_short_id(length):
    short_id = ''
    for _ in range(length):
        symbol = choice([
            chr(randrange(48, 58)),
            chr(randrange(65, 91)),
            chr(randrange(97, 123)),
        ])
        short_id += symbol
    return short_id


def get_unique_short_id(model, length=6):
    short_id = get_short_id(length)
    while model.query.filter_by(short=short_id).first():
        short_id = get_short_id(length)
    return short_id
