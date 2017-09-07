from evoke.interpreter import Interpreter
from subprocess import call
from tempfile import NamedTemporaryFile
import os


class Shell(Interpreter):

    def run(self, script: str):
        tempscript = NamedTemporaryFile("w", delete=False)
        tempscript.write("#!/bin/{}\n".format(self.qualifier))
        tempscript.write(script)
        tempscript.close()
        os.chmod(tempscript.name, 0o700)
        rc = call(tempscript.name)
        os.remove(tempscript.name)

        if rc != 0:
            return False

        return True

def constructor():
    return Shell