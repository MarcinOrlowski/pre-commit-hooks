"""
# composer-lock-in-sync
#
# Verifies that `composer.lock` has been updated after `composer.json`
# was last changed. If either file is absent the hook is a no-op, so
# it is safe to enable in repositories that do not use Composer.
#
# Detection is based on the files' modification times — the moment
# `composer.json` is touched (new dependency added, version bumped,
# …) `composer.lock` must be regenerated to stay consistent.
#
# Copyright ©2021-2026 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/pre-commit-hooks/
#
# Test invocation:
#   pre-commit try-repo . composer-lock-in-sync --verbose --all-files
"""

import argparse
import os
import sys
from typing import Optional, Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description = 'Verifies composer.lock is newer than composer.json.',
    )
    parser.add_argument('--path', action = 'store', dest = 'path', default = '.',
                        help = 'Directory containing composer.json / composer.lock '
                               '(default: current working directory).')
    # pre-commit passes filenames positionally; accept and ignore.
    parser.add_argument('filenames', nargs = '*', help = argparse.SUPPRESS)
    args: argparse.Namespace = parser.parse_args(argv)

    json_path: str = os.path.join(args.path, 'composer.json')
    lock_path: str = os.path.join(args.path, 'composer.lock')

    if not os.path.isfile(json_path) or not os.path.isfile(lock_path):
        return 0

    if os.path.getmtime(lock_path) >= os.path.getmtime(json_path):
        return 0

    print('composer.lock is older than composer.json and must be regenerated.')
    print('To rebuild the lock file, run one of:')
    print('  composer update --lock')
    print('  composer update --lock --ignore-platform-reqs')
    print('')
    print('NOTE: when using containers, the above command should be run inside the container.')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
