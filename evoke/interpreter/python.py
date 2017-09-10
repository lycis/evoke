import importlib.util
import sys
import types

from evoke.interpreter import Interpreter, BadInterpreter


class Python(Interpreter):

    def run(self, script: str):
        if self.qualifier is not None:
            required_version = self.qualifier.split('.')

            if required_version[0] != sys.version_info[0]:
                raise BadInterpreter("python",
                    "required python version does not match executing version ({} vs {})"
                        .format(self.qualifier, sys.version))

            if len(required_version) > 1 and required_version[1] != sys.version_info[1]:
                raise BadInterpreter("python",
                    "requird python version does not match executing version ({} vs {})"
                        .format(self.qualifier,sys.version))

            if len(required_version) > 2 and required_version[2] != sys.version_info[2]:
                raise BadInterpreter("python",
                    "requird python version does not match executing version ({} vs {})"
                        .format(self.qualifier,sys.version))

        file = self.str_to_temporary_file(script)

        loader = importlib.machinery.SourceFileLoader(script.replace("/", "_"), file)
        if loader is None:
            print("Failed to load python snippet ({}).".format(file))
            return False

        mod = types.ModuleType(loader.name)
        loader.exec_module(mod)

        return True




def constructor():
    return Python