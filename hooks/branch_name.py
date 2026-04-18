"""
# branch-name
#
# Verifies the current Git branch name matches a required regular
# expression. Intended to run at `pre-push` stage so attempts to push
# a branch whose name violates the project's naming convention are
# blocked before they reach the remote.
#
# Copyright ©2021-2026 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/pre-commit-hooks/
#
# Test invocation:
#   pre-commit try-repo . branch-name --verbose --hook-stage pre-push
"""

import argparse
import os
import re
import subprocess
import sys
from typing import Any, Dict, List, Optional, Sequence

DEFAULT_CONFIG_PATH: str = '.branch-name.yaml'


def current_branch() -> Optional[str]:
    """
    Returns the name of the currently checked-out branch, or ``None`` if
    HEAD is detached (no symbolic ref).
    """
    result: subprocess.CompletedProcess = subprocess.run(
        ['git', 'symbolic-ref', '--short', '-q', 'HEAD'],
        capture_output = True, text = True,
    )
    if result.returncode != 0:
        return None
    name: str = result.stdout.strip()
    return name or None


def load_config(path: str) -> Dict[str, Any]:
    """
    Loads a YAML config file. Returns an empty dict when the file is
    empty. Raises ``ValueError`` with a user-friendly message on parse
    errors or unexpected top-level shape.
    """
    try:
        import yaml  # PyYAML; declared as a hook dependency.
    except ImportError as exc:
        raise ValueError(
            'PyYAML is required to read the branch-name config file but is '
            'not available in this environment.'
        ) from exc

    with open(path, 'r', encoding = 'utf-8') as handle:
        try:
            data: Any = yaml.safe_load(handle)
        except yaml.YAMLError as exc:
            raise ValueError(f'Cannot parse {path}: {exc}') from exc

    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f'{path}: top level must be a mapping, got {type(data).__name__}.')
    return data


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description = 'Checks current Git branch name against a regular expression.',
    )
    parser.add_argument('-c', '--config', action = 'store', dest = 'config',
                        default = DEFAULT_CONFIG_PATH,
                        help = f'Path to YAML config file (default: {DEFAULT_CONFIG_PATH}). '
                               'The file may define "pattern" (string) and "allow" (list of '
                               'branch names). Missing file is fine as long as --pattern is '
                               'provided on the command line.')
    parser.add_argument('-p', '--pattern', action = 'store', dest = 'pattern', default = None,
                        help = 'Regular expression the branch name must fully match. Overrides '
                               'the "pattern" value from the config file when provided.')
    args: argparse.Namespace = parser.parse_args(argv)

    config: Dict[str, Any] = {}
    if os.path.isfile(args.config):
        try:
            config = load_config(args.config)
        except ValueError as exc:
            print(str(exc))
            return 10
    elif args.config != DEFAULT_CONFIG_PATH:
        print(f'Config file not found: {args.config}')
        return 10

    pattern_str: Optional[str] = args.pattern if args.pattern is not None else config.get('pattern')
    if not pattern_str:
        print('No pattern provided. Set "pattern" in the config file or pass --pattern.')
        return 10
    if not isinstance(pattern_str, str):
        print(f'"pattern" must be a string, got {type(pattern_str).__name__}.')
        return 10

    try:
        pattern: re.Pattern = re.compile(pattern_str)
    except re.error as exc:
        print(f'Invalid pattern regex: {exc}')
        return 10

    raw_allow: Any = config.get('allow', [])
    if not isinstance(raw_allow, list) or not all(isinstance(item, str) for item in raw_allow):
        print('"allow" must be a list of strings.')
        return 10
    allow: List[str] = list(raw_allow)

    branch: Optional[str] = current_branch()
    if branch is None:
        print('Cannot determine current branch (detached HEAD?). Skipping check.')
        return 0

    if branch in allow:
        return 0

    if pattern.fullmatch(branch):
        return 0

    print(f'Branch name "{branch}" does not match required pattern: {pattern_str}')
    if allow:
        print(f'Allowed exceptions: {", ".join(allow)}')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
