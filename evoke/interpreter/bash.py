from evoke.interpreter import Interpreter
from subprocess import call
from tempfile import NamedTemporaryFile
import os


class Bash(Interpreter):

    def run(self, script: str):
        tempscript = NamedTemporaryFile("w", delete=False)
        tempscript.write("#!/bin/bash\n")
        tempscript.write(script)
        tempscript.close()
        os.chmod(tempscript.name, 0o700)
        rc = call(tempscript.name)
        os.remove(tempscript.name)

        if rc != 0:
            return False

        return True

def build() -> Bash:
    return Bash()