"""
# no-ai-slop
#
# Scans modified text files for "forbidden" typographic characters commonly
# introduced by AI text generators (em/en dashes, curly quotes, non-breaking
# and zero-width spaces). Fails (non-zero exit) when any is found, reporting
# the file, line, column, code point and Unicode name. No autofix.
#
# Copyright ©2021-2026 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/pre-commit-hooks/
#
# Test invocation:
#   pre-commit try-repo . no-ai-slop --verbose --all-files
"""

import argparse
import sys
import unicodedata
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

# Default set of forbidden characters. Ellipsis (U+2026) is deliberately NOT
# included. Override with --chars to supply a different set per repository.
DEFAULT_FORBIDDEN_CHARS: str = (
    '—'  # EM DASH
    '–'  # EN DASH
    '“'  # LEFT DOUBLE QUOTATION MARK
    '”'  # RIGHT DOUBLE QUOTATION MARK
    '‘'  # LEFT SINGLE QUOTATION MARK
    '’'  # RIGHT SINGLE QUOTATION MARK
    ' '  # NO-BREAK SPACE
    '​'  # ZERO WIDTH SPACE
)


def describe_char(char: str) -> str:
    """Returns a human-readable label, e.g. 'U+2014 (EM DASH)'."""
    name: str = unicodedata.name(char, 'UNKNOWN CHARACTER')
    return f'U+{ord(char):04X} ({name})'


def scan_file(filename: str, forbidden: str) -> List[Tuple[int, int, str]]:
    """
    Scans a single file for forbidden characters.

    :return: list of (line_number, column, char) tuples; 1-based line/column.
    """
    forbidden_set = set(forbidden)
    hits: List[Tuple[int, int, str]] = []
    with open(filename, mode = 'r', encoding = 'utf-8') as fh:
        for line_no, line in enumerate(fh, start = 1):
            for col, char in enumerate(line.rstrip('\n').rstrip('\r'), start = 1):
                if char in forbidden_set:
                    hits.append((line_no, col, char))
    return hits


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--chars', action = 'store', dest = 'chars', default = DEFAULT_FORBIDDEN_CHARS,
                        help = 'The set of characters to forbid. Defaults to common AI-slop typographic characters.')
    parser.add_argument('filenames', nargs = '*', help = 'Filenames to scan')
    args: argparse.Namespace = parser.parse_args(argv)

    if args.chars == '':
        print('Invalid --chars value: empty set')
        return 10

    return_code: int = 0
    for filename in args.filenames:
        try:
            hits: List[Tuple[int, int, str]] = scan_file(filename, args.chars)
        except UnicodeDecodeError:
            print(f'[SKIP] {filename}: not valid UTF-8 text')
            continue
        except OSError as ex:
            print(f'[ERROR] {filename}: {ex}')
            return_code = 1
            continue

        for line_no, col, char in hits:
            print(f'{filename}:{line_no}:{col}: forbidden character {describe_char(char)}')
            return_code = 1

    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
