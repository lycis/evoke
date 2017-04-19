from pathlib import Path
from os.path import dirname
from evoke.snippets import anchor as internal_lib_anchor
import json


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
