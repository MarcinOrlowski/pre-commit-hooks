"""
# commit-msg
#
# Enforces the shape of the commit message: how many lines it may span
# and how long each of these lines may be. Intended to run at the
# `commit-msg` stage, where Git hands the message file over before the
# commit is created.
#
# By default only a single line (the subject) is allowed, and no line
# may exceed 100 characters.
#
# Copyright ©2021-2026 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/pre-commit-hooks/
#
# Test invocation:
#   pre-commit try-repo . commit-msg --verbose --hook-stage commit-msg \
#       --commit-msg-filename .git/COMMIT_EDITMSG
"""

import argparse
import subprocess
import sys
from typing import List, Optional, Sequence

DEFAULT_MAX_LINES: int = 1
DEFAULT_MAX_LENGTH: int = 100
DEFAULT_COMMENT_CHAR: str = '#'


def comment_char() -> str:
    """
    Returns the comment character Git strips message lines by, as set by
    `core.commentChar`. Falls back to '#' when unset, when the value is
    'auto' (Git picks a character at runtime, '#' in the vast majority of
    cases) or when Git is not callable at all.
    """
    try:
        result: subprocess.CompletedProcess = subprocess.run(
            ['git', 'config', '--get', 'core.commentChar'],
            capture_output = True, text = True,
        )
    except OSError:
        return DEFAULT_COMMENT_CHAR

    if result.returncode != 0:
        return DEFAULT_COMMENT_CHAR
    value: str = result.stdout.strip()
    if not value or value == 'auto':
        return DEFAULT_COMMENT_CHAR
    return value


def is_scissors_line(line: str, char: str) -> bool:
    """
    Tells if the line is Git's "scissors" separator, i.e.

        # ------------------------ >8 ------------------------

    Everything below it (the diff `git commit --verbose` appends, or the
    part cut off by `commit.cleanup=scissors`) is not part of the message.
    """
    stripped: str = line.strip()
    if not stripped.startswith(char):
        return False
    body: str = stripped[len(char):].strip()
    if '>8' not in body and '8<' not in body:
        return False
    return body.count('-') >= 8 and set(body) <= set('->8< ')


def normalize(text: str, char: str) -> List[str]:
    """
    Reduces the raw contents of the commit message file to the lines that
    actually end up in the commit, mimicking Git's default cleanup mode:
    everything from the scissors line down is dropped, comment lines are
    removed, trailing whitespace is stripped, consecutive empty lines are
    collapsed into one, and leading/trailing empty lines are removed.

    :return: the message lines, without line terminators.
    """
    lines: List[str] = []
    for line in text.splitlines():
        if is_scissors_line(line, char):
            break
        if line.startswith(char):
            continue
        lines.append(line.rstrip())

    collapsed: List[str] = []
    for line in lines:
        if not line and collapsed and not collapsed[-1]:
            continue
        collapsed.append(line)

    while collapsed and not collapsed[0]:
        collapsed.pop(0)
    while collapsed and not collapsed[-1]:
        collapsed.pop()

    return collapsed


def parse_limit(value: str, option: str) -> int:
    """
    Parses a limit argument. Raises ``ValueError`` with a user-friendly
    message when the value is not a non-negative integer.
    """
    try:
        limit: int = int(value)
    except ValueError:
        raise ValueError(f'Invalid {option} value: "{value}". Expected a non-negative integer.')
    if limit < 0:
        raise ValueError(f'Invalid {option} value: "{value}". Expected a non-negative integer.')
    return limit


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description = 'Checks commit message line count and line length.',
    )
    parser.add_argument('-n', '--max-lines', action = 'store', dest = 'max_lines',
                        default = str(DEFAULT_MAX_LINES),
                        help = f'Maximum number of lines the commit message may span '
                               f'(default: {DEFAULT_MAX_LINES}). Use 0 for no limit.')
    parser.add_argument('-w', '--max-length', action = 'store', dest = 'max_length',
                        default = str(DEFAULT_MAX_LENGTH),
                        help = f'Maximum length of a single commit message line, in characters '
                               f'(default: {DEFAULT_MAX_LENGTH}). Use 0 for no limit.')
    parser.add_argument('filenames', nargs = '*', help = 'Path to the commit message file.')
    args: argparse.Namespace = parser.parse_args(argv)

    try:
        max_lines: int = parse_limit(args.max_lines, '--max-lines')
        max_length: int = parse_limit(args.max_length, '--max-length')
    except ValueError as exc:
        print(str(exc))
        return 10

    if len(args.filenames) != 1:
        print('Expected exactly one commit message file, '
              f'got {len(args.filenames)}.')
        print('This hook must run at the "commit-msg" stage: stages: [ commit-msg ]')
        return 10

    filename: str = args.filenames[0]
    try:
        with open(filename, mode = 'r', encoding = 'utf-8') as fh:
            text: str = fh.read()
    except OSError as exc:
        print(f'Cannot read commit message file {filename}: {exc}')
        return 10

    lines: List[str] = normalize(text, comment_char())
    if not lines:
        # Empty message; Git aborts the commit on its own.
        return 0

    return_code: int = 0

    if max_lines and len(lines) > max_lines:
        print(f'Commit message spans {len(lines)} lines, '
              f'while at most {max_lines} {"is" if max_lines == 1 else "are"} allowed.')
        return_code = 1

    if max_length:
        for line_no, line in enumerate(lines, start = 1):
            if len(line) > max_length:
                print(f'Commit message line {line_no} is {len(line)} characters long, '
                      f'exceeding the limit of {max_length}.')
                print(f'  | {line}')
                return_code = 1

    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
