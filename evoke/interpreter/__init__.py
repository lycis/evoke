class Interpreter:
    pass


class BadInterpreter(Exception):
    """
    Indicates that the given interpreter does not exist
    """

    def __init__(self, type: str):
        self.type = type


def create_interpreter(type: str, script: str) -> Interpreter:
    """
    Creates a new interpreter of the given type to run a snippet.

    :param type: interpreter type (e.g. bash, groovy, ...)
    :param script: the script that the interpreter shall be prepared to run
    :return: instance of the fitting interpreter type
    """
    raise BadInterpreter(type)