import argparse
import os
from typing import IO
from typing import Optional
from typing import Sequence


def fix_file(args, file_obj: IO[bytes]) -> int:
    """
    Test for newline at end of file Empty files will throw IOError here

    :param file_obj:
    """
    try:
        file_obj.seek(-1, os.SEEK_END)
    except OSError:
        return 0

    last_character = file_obj.read(1)
    # last_character will be '' for an empty file
    if last_character not in {b'\n', b'\r'} and last_character != b'':
        if args.fix:
            # Needs this seek for windows, otherwise IOError
            file_obj.seek(0, os.SEEK_END)
            file_obj.write(b'\n')
        return 1

    while last_character in {b'\n', b'\r'}:
        # Deal with the beginning of the file
        if file_obj.tell() == 1:
            if args.fix:
                # If we've reached the beginning of the file and it is all
                # linebreaks then we can make this file empty
                file_obj.seek(0)
                file_obj.truncate()
            return 1

        # Go back two bytes and read a character
        file_obj.seek(-2, os.SEEK_CUR)
        last_character = file_obj.read(1)

    # Our current position is at the end of the file just before any amount of
    # newlines.  If we find extraneous newlines, then backtrack and trim them.
    position = file_obj.tell()
    remaining = file_obj.read()
    for sequence in (b'\n', b'\r\n', b'\r'):
        if remaining == sequence:
            return 0
        elif remaining.startswith(sequence):
            if args.fix:
                file_obj.seek(position + len(sequence))
                file_obj.truncate()
            return 1

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--fix', action = 'store', dest = 'fix', default = "no",
                        help = 'Corrects invalid files in-place. Supported values: "yes", "no" (default).')
    parser.add_argument('filenames', nargs = '*', help = 'Filenames to fix')
    args = parser.parse_args(argv)

    if args.fix not in ["yes", "no"]:
        print(f'Invalid --fix value: {args.fix}')
        return 10
    args.fix = args.fix == "yes"


    retv = 0

    for filename in args.filenames:
        # Read as binary so we can read byte-by-byte
        with open(filename, 'rb+') as file_obj:
            ret_for_file = fix_file(args, file_obj)
            if ret_for_file:
                print(f'Fixing {filename}')
            retv |= ret_for_file

    return retv


if __name__ == '__main__':
    exit(main())
