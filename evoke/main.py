import argparse
import os.path
from pathlib import Path
from evoke.library import init as init_evoke


class LibraryNotFound(Exception):

    def __init__(self, path):
        self.path = path
        super(LibraryNotFound, self).__init__(path)


def main():
    global args
    parse_args()

    if args.verbose:
        print("recalling evocation '{0}'...\n".format(args.evocation))

    try:
        library = load_library(args.evocation)
    except LibraryNotFound as e:
        print("library '{}' not found\n".format(e.path))


def parse_args():
    global args
    parser = argparse.ArgumentParser(prog='evoke',
                                     description='summon powerful evocations from your tomes of knowlegde')
    parser.add_argument('evocation', type=str, help='name of the evocation you want to call')
    parser.add_argument('-l, --library', type=str, dest='library', help='path to the evocations library',
                        default=os.path.expanduser("~"))
    parser.add_argument('-v, --verbose', dest='verbose', action='store_true')
    args = parser.parse_args()


def load_library(evocation: str) -> dict:
    """
    loads the library for the given evocation, or the users default library
    when no evokelib is given
    :param evocation: evocation id
    :return: dict containing the library information
    """
    global args

    lib_path = '/'.join(evocation.split('/')[:-1])

    if args.verbose:
        print('loading library path: {0}'.format(lib_path))

    candidates = [
        Path.cwd() / '.evoke/lib/',
        Path.home() / '.evoke/lib/',
        Path(os.path.dirname(init_evoke.__file__))
    ]

    library_dir = None
    for c in candidates:
        ld = c / lib_path
        if ld.exists():
            library_dir = ld
            break

    if library_dir is None:
        raise LibraryNotFound(lib_path)

    return {}


if __name__ == '__main__':
    main()
