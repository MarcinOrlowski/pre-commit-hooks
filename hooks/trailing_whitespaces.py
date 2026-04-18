#
# pre-commit-hooks
#
# Copyright ©2021-2025 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/pre-commit-hooks/
#

import argparse
import os
import sys
from typing import Optional
from typing import Sequence
from typing import List
from typing import IO


def gen_tmp_filename(filename: str, suffix: str = 'tmp') -> str:
    idx: int = 0
    while True:
        result_name: str = f'{filename}.{suffix}-{idx}'
        try:
            fd: int = os.open(result_name, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            idx += 1
            continue
        os.close(fd)
        return result_name


def fix_file(args: argparse.Namespace, filename: str, is_markdown: bool, chars: Optional[bytes]) -> bool:
    with open(filename, mode = 'rb') as rfh:
        lines: List[bytes] = rfh.readlines()
    new_lines: List[bytes] = [process_line(line, is_markdown, chars) for line in lines]
    if new_lines == lines:
        return False

    if args.fix:
        save_filename: str = gen_tmp_filename(filename)
        with open(save_filename, mode = 'wb') as wfh:
            wfh.writelines(new_lines)

        bak_filename: str = gen_tmp_filename(filename, 'bak')
        os.rename(filename, bak_filename)
        os.rename(save_filename, filename)
        os.unlink(bak_filename)

    return True


def process_line(line: bytes, is_markdown: bool, chars: Optional[bytes]) -> bytes:
    if line[-2:] == b'\r\n':
        eol: bytes = b'\r\n'
        line = line[:-2]
    elif line[-1:] == b'\n':
        eol: bytes = b'\n'
        line = line[:-1]
    else:
        eol: bytes = b''
    # preserve trailing two-space for non-blank lines in markdown files
    if is_markdown and (not line.isspace()) and line.endswith(b'  '):
        return line[:-2].rstrip(chars) + b'  ' + eol
    return line.rstrip(chars) + eol


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--fix', action = 'store', dest = 'fix', default = "no",
                        help = 'Corrects invalid files in-place. Supported values: "yes", "no" (default).')
    parser.add_argument('--no-markdown-linebreak-ext', action = 'store_true', help = argparse.SUPPRESS)
    parser.add_argument('--markdown-linebreak-ext', action = 'append', default = [], metavar = '*|EXT[,EXT,...]',
                        help = 'Markdown extensions (or *) to not strip linebreak spaces. default: %(default)s')
    parser.add_argument('--chars',
                        help = 'The set of characters to strip from the end of lines. Defaults to all whitespace characters.')
    parser.add_argument('filenames', nargs = '*', help = 'Filenames to fix')
    args: argparse.Namespace = parser.parse_args(argv)

    if args.fix not in ["yes", "no"]:
        print(f'Invalid --fix value: {args.fix}')
        return 10
    args.fix: bool = args.fix == "yes"

    if args.no_markdown_linebreak_ext:
        print('--no-markdown-linebreak-ext now does nothing!')

    md_args: List[str] = args.markdown_linebreak_ext
    if '' in md_args:
        parser.error('--markdown-linebreak-ext requires a non-empty argument')
    all_markdown: bool = '*' in md_args
    # normalize extensions; split at ',', lowercase, and force 1 leading '.'
    md_exts: List[str] = [
        '.' + x.lower().lstrip('.') for x in ','.join(md_args).split(',')
    ]

    # reject probable "eaten" filename as extension: skip leading '.' with [1:]
    for ext in md_exts:
        if any(c in ext[1:] for c in r'./\:'):
            parser.error(
                f'bad --markdown-linebreak-ext extension '
                f'{ext!r} (has . / \\ :)\n'
                f"  (probably filename; use '--markdown-linebreak-ext=EXT')",
            )
    chars: Optional[bytes] = None if args.chars is None else args.chars.encode()
    return_code: int = 0
    for filename in args.filenames:
        _, extension = os.path.splitext(filename.lower())
        md: bool = all_markdown or extension in md_exts
        try:
            needs_fix: bool = fix_file(args, filename, md, chars)
        except OSError as ex:
            print(f'[ERROR] {filename}: {ex}')
            return_code = 1
            continue
        if needs_fix:
            if args.fix:
                print(f'Fixed {filename}')
            else:
                print(f'[ERROR] {filename}')
            return_code = 1
    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
