import argparse
import os.path


def main():
    global args
    parse_args()

    if args.verbose:
        print("recalling evocation '{0}'...\n".format(args.evocation))

    library = load_library(args.evocation)

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

    lib_path = evocation.split('/')[:-1]

    if args.verbose:
        print('loading library path: {0}'.format(lib_path))



    return {}

if __name__ == '__main__':
    main()
