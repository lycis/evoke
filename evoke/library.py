from pathlib import Path
from os.path import dirname

from evoke.interpreter import create_interpreter
from evoke.snippets import anchor as internal_lib_anchor
import json


class Snippet:
    """
    Represents a code snippet and is stringy.
    """

    def __init__(self, name: str, content: str):
        self.name = name # type: str
        self.interpreter_type = "python" # type: str

        ca = content.split('\n')
        if ca[0].startswith('#!'):
            self.interpreter_type = ca.pop(0)[2:]

        self.content = content # type: str


    def interpreter(self):
        return create_interpreter(self.interpreter_type, self.content)


class LibraryNotFound(Exception):
    """
    Indicates that a given library could not be found
    """
    def __init__(self, path):
        self.path = path
        super(LibraryNotFound, self).__init__(path)


class BrokenLibrary(Exception):
    """
    Indicates that a loaded library somehow broken or
    corrupted.
    """

    def __init__(self, name, error):
        self.name = name
        self.error = error


class Library:
    """
    Provides access to a snippet library.
    """

    def __init__(self, libname: str):
        self._dir = _find_library_dir(libname) # type: Path
        self.name = libname # type: str
        self._parse_index()


    def _parse_index(self):
        """
        Reads the library index and builds the library from the
        index data.
        """

        index_file = self._dir / 'index.json'
        if not index_file.exists():
            raise BrokenLibrary(self.name, 'missing index')

        if not index_file.is_file():
            raise BrokenLibrary(self.name, 'index not a file')

        with index_file.open('rt') as data:
            try:
                self.index = json.load(data)
            except json.JSONDecodeError as e:
                raise BrokenLibrary(self.name, e.msg)

#       some sanity checks for the index
        if "description" in self.index and not isinstance(self.index['description'], str):
            raise BrokenLibrary(self.name, 'description is not a string')

        if not 'snippets' in self.index:
            raise BrokenLibrary(self.name, 'index is missing snippets data')

        if not isinstance(self.index['snippets'], dict):
            raise BrokenLibrary(self.name, 'index snippets entry not a map')



    def description(self) -> str:
        """
        Returns the description of the library if set or an empty
        string if not given.

        :return: description of the library if set
        """

        if not 'description' in self.index:
            return ''

        return self.index['description']

    def snippet(self, name: str) -> Snippet:
        """
        Gives the content of a snippet.

        When necessary the content will be downloaded from a
        remote destination or a file when the content if required.

        :param name: name of the snippet
        :return: content of the snippet (or None if a snippet
                 of that name does not exist)
        """

        if not name in self.index['snippets']:
            return None

        # TODO load from other destinations
        if not 'content' in self.index['snippets'][name]:
            return None

        snippet_data = self.index['snippets'][name]
        content =  snippet_data['content']
        s = Snippet(name, content)

        if 'interpreter' in snippet_data:
            if not isinstance(snippet_data['interpreter'], str):
                raise BrokenLibrary(self.name, 'interpreter of {} is not string'.format(name))

            s.interpreter_type = snippet_data['interpreter']

        return s

    def __getitem__(self, item):
        return self.snippet(item)


def _find_library_dir(libname: str) -> str:
    """
    returns the first matching path for the library that includes
    the library
    :param evocation:
    :return:
    """

    candidates = [
        Path.cwd() / '.evoke/lib/',
        Path.home() / '.evoke/lib/',
        Path(dirname(internal_lib_anchor.__file__))
    ]

    library_dir = None
    for c in candidates:
        ld = c / libname
        if ld.exists():
            library_dir = ld
            break

    if library_dir is None:
        raise LibraryNotFound(libname)

    return library_dir

