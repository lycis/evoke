from importlib import import_module


class InterpreterImplementationError(Exception):

    def __init__(self, error):
        self.error = error


class Interpreter:

    def run(self, script: str):
        raise InterpreterImplementationError("method run(script) not implemented")


class BadInterpreter(Exception):
    """
    Indicates that the given interpreter does not exist
    """

    def __init__(self, type: str, reason: str = None):
        self.type = type
        self.reason = reason


def create_interpreter(type: str, script: str) -> Interpreter:
    """
    Creates a new interpreter of the given type to run a snippet.

    :param type: interpreter type (e.g. bash, groovy, ...)
    :param script: the script that the interpreter shall be prepared to run
    :return: instance of the fitting interpreter type
    """

    ip = None
    try:
        mod = import_module("evoke.interpreter.{}".format(type))
    except ImportError as e:
        raise BadInterpreter(type)

    ip = mod.build()

    if ip is None:
        raise BadInterpreter(type)

    if not isinstance(ip, Interpreter):
        raise BadInterpreter(type, "interpreter object has wrong type")

    return ip


class InterpreterError(Exception):
    """
    This exception type indicates that an internal error occurred in the
    interpreter. This might be e.g. that required binaries were not found
    or something else that is preventing the interpreter from running.

    It does *not* indicate an error related to the execution of a script
    by the interpreter!
    """

    def __init__(self, reason: str):
        self.reason = reason
