from evoke.interpreter import Interpreter
from subprocess import call
from tempfile import NamedTemporaryFile
import os


class Shell(Interpreter):

    def run(self, script: str):
        name = self.str_to_temporary_file("#!/bin/{}\n{}".format(self.qualifier, script))
        os.chmod(name, 0o700)
        rc = call(name)
        if rc != 0:
            return False
        return True

def constructor():
    return Shell