from evoke.interpreter import Interpreter


class Bash(Interpreter):

    def run(self, script: str):
        print("running bash script")

def build() -> Bash:
    return Bash()