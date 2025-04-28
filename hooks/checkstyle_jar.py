"""
# checkstyle-jar
#
# Bridges Checkstyle code linter with pre-commit. This hook requires
# JAR version of Checkstyle and Java environment installed (in $PATH)
#
# Copyright ©2021-2025 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/pre-commit-hooks/
#
# Test invocation:
#   pre-commit try-repo . checkstyle-jar --verbose --all-files
"""

import argparse
import pathlib
import sys
from pathlib import Path
from subprocess import run, CompletedProcess
from urllib import request, parse
from urllib.parse import ParseResult
from http.client import HTTPMessage
from typing import List, Optional, Sequence

RC_OK: int = 0
RC_ERROR: int = 1
RC_FAKE_ERROR_CODE: int = 10
RC_DOWNLOAD_ERROR: int = 20
RC_NO_JAR: int = 150


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument(
        '--cache', action = 'store', dest = 'cache', nargs = 1, metavar = 'DIR',
        default = ['~/.cache/pre-commit'],
        help = 'Path to shared cache directory to use to store downloaded JAR file.')
    command_group.add_argument(
        '--jar', action = 'store', dest = 'jar', nargs = 1, metavar = 'FILE',
        help = 'Path to Checkstyle JAR file, incl. JAR file name.')
    command_group.add_argument(
        '--jar-url', action = 'store', dest = 'jar_url', nargs = 1, metavar = 'URL',
        help = 'URL to downloadable Checkstyle JAR file.')
    parser.add_argument(
        '--config', dest = 'config', nargs = 1, action = 'store', metavar = "PATH", default = '/google_checks.xml',
        help = 'Path to checkstyle config to use. Use "/google_checks.xml" or "/sun_checks.xml" to use built-in styles.')
    parser.add_argument('files', nargs = '*', help = 'Files to check.')
    args: argparse.Namespace = parser.parse_args(argv)

    if args.jar_url:
        args.jar_url: str = args.jar_url[0]

    # https://github.com/checkstyle/checkstyle/releases/
    if args.jar:
        args.jar: Path = Path(args.jar[0]).expanduser()

    if not args.jar_url and not args.jar:
        args.jar_url: str = 'https://github.com/checkstyle/checkstyle/releases/download/checkstyle-10.23.1/checkstyle-10.23.1-all.jar'
    args.cache: Path = Path(args.cache[0]).expanduser()
    if not args.cache.is_dir():
        print(f'The --cache must point to writable directory: {args.cache}')
        return RC_ERROR

    if not args.files:
        return RC_OK

    if args.jar_url:
        parsed_url: ParseResult = parse.urlparse(args.jar_url)
        downloaded_jar_filename: str = pathlib.Path(parsed_url.path).name
        downloaded_jar_path: Path = Path(args.cache).expanduser() / downloaded_jar_filename
        downloaded_tmp_path: Path = Path(args.cache).expanduser() / f'{downloaded_jar_filename}.tmp'
        if not downloaded_jar_path.exists():
            print(f'Downloading {downloaded_jar_filename} to {args.cache}...')
            path: str
            http: HTTPMessage
            path, http = request.urlretrieve(args.jar_url, downloaded_tmp_path)
            tmp_path: Path = Path(path)
            if not tmp_path.exists():
                print(f'Failed to download JAR file: {args.jar_url}')
                return RC_DOWNLOAD_ERROR
            tmp_path.rename(downloaded_jar_path)

        if downloaded_jar_path.exists():
            args.jar: Path = downloaded_jar_path

    if not args.jar.exists():
        print(f'Checkstyle JAR file not found: {args.jar}')
        print(' '.join([
            'See download page: https://github.com/checkstyle/checkstyle/releases/',
            'or use --jar-url and point to downloadable JAR file.', ]))
        return RC_NO_JAR

    # https://checkstyle.sourceforge.io/cmdline.html#Download_and_Run
    cmd: List[str] = ['java', '-jar', str(args.jar), '-c', args.config] + args.files

    completed: CompletedProcess = run(cmd, capture_output = True)
    return_code: int = completed.returncode

    stdout: List[str] = list(filter(lambda item: item != '', completed.stdout.decode().split('\n')))
    stderr: List[str] = list(filter(lambda item: item != '', completed.stderr.decode().split('\n')))
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
