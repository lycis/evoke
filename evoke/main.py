import argparse
import os.path
from library import Library, LibraryNotFound, BrokenLibrary


def main():
    global args
    parse_args()

    if args.verbose:
        print("recalling evocation '{0}'...\n".format(args.evocation))

    library = None
    lib_path = '/'.join(args.evocation.split('/')[:-1])
    if args.verbose:
        print('loading library: {0}'.format(lib_path))
    try:
        library = Library(lib_path)
    except LibraryNotFound as e:
        print("library '{}' not found\n".format(e.path))
        exit(1)
    except BrokenLibrary as e:
        print("failed to load library '{}': {}\n".format(e.name, e.error))
        exit(1)

    snippet_name = args.evocation.split('/')[-1]
    if args.verbose:
        print("retrieving content of snippet '{}'\n".format(snippet_name))

    snippet = library[snippet_name]
    if snippet is None:
        print("no such evocation\n")
        exit(1)

    print("Content:\n{}\n".format(snippet))



def parse_args():
    global args
    parser = argparse.ArgumentParser(prog='evoke',
                                     description='summon powerful evocations from your tomes of knowlegde')
    parser.add_argument('evocation', type=str, help='name of the evocation you want to call')
    parser.add_argument('-l, --library', type=str, dest='library', help='path to the evocations library',
                        default=os.path.expanduser("~"))
    parser.add_argument('-v, --verbose', dest='verbose', action='store_true')
    args = parser.parse_args()





if __name__ == '__main__':
    main()
