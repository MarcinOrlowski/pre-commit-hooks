"""
# no-op
#
# No-OP hook (dev tool). Does nothing and always returns success.
# Most likely useless for non development purposes only. I use it
# because pre-commit do not allow `.pre-commit-options.yaml` to
# feature repository with no hook from it used.
#
# Copyright ©2021-2025 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/pre-commit-hooks/
#
"""

import sys
from typing import Optional, Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
