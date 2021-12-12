
def get_id():
    x = 0
    while True:
        yield x
        x += 1


generator = get_id()
