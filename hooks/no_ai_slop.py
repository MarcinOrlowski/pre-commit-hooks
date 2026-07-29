"""
# no-ai-slop
#
# Scans modified text files for "forbidden" typographic characters commonly
# introduced by AI text generators (em/en dashes, curly quotes, exotic spaces,
# invisible format and bidirectional control characters). Fails (non-zero
# exit) when any is found, reporting
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

# Default set of forbidden characters. Ellipsis (U+2026), guillemets (U+00AB,
# U+00BB, legitimate in i.e. French or Polish prose) and ZERO WIDTH JOINER
# (U+200D, legitimate in emoji sequences) are deliberately NOT included.
# Override with --chars to supply a different set per repository.
#
# Invisible characters are spelled as escapes on purpose, to keep this source
# readable and greppable.
DEFAULT_FORBIDDEN_CHARS: str = (
    # Quotation marks and primes
    '“'  # LEFT DOUBLE QUOTATION MARK
    '”'  # RIGHT DOUBLE QUOTATION MARK
    '„'  # DOUBLE LOW-9 QUOTATION MARK
    '‟'  # DOUBLE HIGH-REVERSED-9 QUOTATION MARK
    '‘'  # LEFT SINGLE QUOTATION MARK
    '’'  # RIGHT SINGLE QUOTATION MARK
    '‚'  # SINGLE LOW-9 QUOTATION MARK
    '‛'  # SINGLE HIGH-REVERSED-9 QUOTATION MARK
    '′'  # PRIME
    '″'  # DOUBLE PRIME

    # Dashes, hyphens and their lookalikes
    '—'  # EM DASH
    '–'  # EN DASH
    '‐'  # HYPHEN
    '‑'  # NON-BREAKING HYPHEN
    '‒'  # FIGURE DASH
    '―'  # HORIZONTAL BAR
    '−'  # MINUS SIGN

    # Spaces
    '\u00A0'  # NO-BREAK SPACE
    '\u2002'  # EN SPACE
    '\u2003'  # EM SPACE
    '\u2007'  # FIGURE SPACE
    '\u2009'  # THIN SPACE
    '\u202F'  # NARROW NO-BREAK SPACE
    '\u205F'  # MEDIUM MATHEMATICAL SPACE
    '\u3000'  # IDEOGRAPHIC SPACE

    # Invisible format characters
    '\u00AD'  # SOFT HYPHEN
    '\u200B'  # ZERO WIDTH SPACE
    '\u200C'  # ZERO WIDTH NON-JOINER
    '\u2060'  # WORD JOINER
    '\uFEFF'  # ZERO WIDTH NO-BREAK SPACE (BOM)

    # Bidirectional controls ("Trojan Source", CVE-2021-42574)
    '\u202A'  # LEFT-TO-RIGHT EMBEDDING
    '\u202B'  # RIGHT-TO-LEFT EMBEDDING
    '\u202C'  # POP DIRECTIONAL FORMATTING
    '\u202D'  # LEFT-TO-RIGHT OVERRIDE
    '\u202E'  # RIGHT-TO-LEFT OVERRIDE
    '\u2066'  # LEFT-TO-RIGHT ISOLATE
    '\u2067'  # RIGHT-TO-LEFT ISOLATE
    '\u2068'  # FIRST STRONG ISOLATE
    '\u2069'  # POP DIRECTIONAL ISOLATE
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
