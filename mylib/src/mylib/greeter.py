from cowsay import say


def make() -> str:
    msg = say("Hello!")
    return msg
