from importlib import import_module
from tempfile import NamedTemporaryFile

import os


class InterpreterImplementationError(Exception):

    def __init__(self, error):
        self.error = error


class Interpreter:
    """
    This class is the base for all interpreters that are
    available. It provides some basic, common functions and defines
    the *run* entry point that interpretes will use.
    """

    def __init__(self, qualifier: str):
        self.qualifier = qualifier
        self.tempfiles = []

    def run(self, script: str):
        raise InterpreterImplementationError("method run(script) not implemented")

    def str_to_temporary_file(self, content) -> str:
        """
        Stores the given content into a temporary file and
        will return the name of it. It will be cleaned when
        the interpreter context is closed.

        :param content: file content
        :return: name of the generated file
        """

        tempscript = NamedTemporaryFile("w", delete=False)
        tempscript.write(content)
        tempscript.close()
        self.tempfiles.append(tempscript.name)
        return tempscript.name

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        for f in self.tempfiles:
            os.remove(f)


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
    qualifier = None
    if ":" in type:
        qualifier = ":".join(type.split(":")[1:])
        type = type.split(":")[0]

    ip = None
    try:
        mod = import_module("evoke.interpreter.{}".format(type))
    except ImportError as e:
        raise BadInterpreter(type)

    constructor = mod.constructor()

    if constructor is None:
        raise BadInterpreter(type)

    return constructor(qualifier)


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
