"""
# checkstyle-jar
#
# Bridges Checkstyle code linter with pre-commit. This hook requires
# JAR version of Checkstyle and Java environment installed (in $PATH)
#
# Copyright ©2021 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/pre-commit-hooks/
#
# Test invocation:
#   pre-commit try-repo . checkstyle-jar --verbose --all-files
"""
from __future__ import print_function

import argparse
import sys
from pathlib import Path
from subprocess import run

RC_OK = 0
RC_ERROR = 1
RC_FAKE_ERROR_CODE = 10
RC_NO_JAR = 150


def main(argv = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--jar', action = 'store', dest = 'jar', nargs = 1, metavar = 'FILE',
                        help = 'Path to Checkstyle JAR file, incl. JAR file name.')
    parser.add_argument('files', nargs = '*', help = 'Files to check.')
    args = parser.parse_args(argv)

    if not args.files:
        return RC_OK

    # https://github.com/checkstyle/checkstyle/releases/
    checkstyle_jar = Path(args.jar[0]) if args.jar else Path('checkstyle-9.0-all.jar')

    if not checkstyle_jar.exists():
        print(f'Checkstyle JAR file not found: {checkstyle_jar}')
        print('See download page: https://github.com/checkstyle/checkstyle/releases/');
        return RC_NO_JAR

    # https://checkstyle.sourceforge.io/cmdline.html#Download_and_Run
    cmd = ['java', '-jar', checkstyle_jar, '-c', '/google_checks.xml'] + args.files

    completed = run(cmd, capture_output = True)
    return_code = completed.returncode

    stdout = list(filter(lambda item: item != '', completed.stdout.decode().split('\n')))
    stderr = list(filter(lambda item: item != '', completed.stderr.decode().split('\n')))
    if stderr:
        print("\n".join(stderr))

    if stdout:
        if stdout[0] == 'Starting audit...':
            del (stdout[0])
        if stdout[-1] == 'Audit done.':
            del (stdout[-1])

        if return_code == RC_OK and stdout:
            return_code = RC_FAKE_ERROR_CODE
        print("\n".join(stdout))

    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
