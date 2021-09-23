# Pre-commit git hooks

Git hooks to integrate with [pre-commit](http://pre-commit.com/).

<!--TOC-->

- [Configure pre-commit](#configure-pre-commit)
- [Two ways to invoke pre-commit](#two-ways-to-invoke-pre-commit)
- [Available hooks](#available-hooks)
  - [`checkstyle-jar`](#checkstyle-jar)
  - [`end-of-file`](#end-of-file)
  - [`trailing-whotespaces`](#trailing-whitespaces)
- [License](#license)

<!--TOC-->

## Configure pre-commit

:warning: These hooks now require Python3.

Add to `.pre-commit-config.yaml` in your git repo:

```
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: 1.0.0  # or any specific git tag
  hooks:
    - id: checkstyle-jar
      args: [ '--jar=/path/to/checkstyle.jar' ]
```

Note, you must configure this hook before use. JAR file can be downloaded from their official
[Checkstyle releases](https://github.com/checkstyle/checkstyle/releases/) section.

## Two ways to invoke pre-commit

If you want to invoke the checks as a git pre-commit hook, run:

    pre-commit install

If you want to run the checks on-demand (outside of git hooks), run:

    pre-commit run --all-files --verbose

## Available hooks

### `checkstyle-jar`

Uses [CheckStyle](https://checkstyle.org/) linter against Java source codes. Contrary to other implementations this one **
requires** CheckStyle JAR file to be given, instead of using system wide available application. This hook expects `java` binary to
be in `$PATH`.

#### Arguments ####

* `--jar` path to the Checkstyle JAR file. If not specified, looks for `checkstyle-9.0-all.jar` in project directory.

#### Example ####

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    # Checks modified Java files with Checkstyle linter.
    - id: checkstyle-jar
      args: [ '--jar=/path/to/checkstyle.jar' ]
```

## `end-of-file` ##

Makes sure files end in a newline and only a newline.

## License ##

* Written and copyrighted &copy;2021 by Marcin Orlowski <mail (#) marcinorlowski (.) com>
* This is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT).
