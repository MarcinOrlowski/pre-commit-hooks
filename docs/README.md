![pre-commit-hooks logo](../artwork/logo.png)

Handy Git hooks to integrate with [pre-commit](http://pre-commit.com/) framework.

---

<!--TOC-->

* [« Main README](../README.md)
* [Configure pre-commit](#configure-pre-commit)
* [Two ways to invoke pre-commit](#two-ways-to-invoke-pre-commit)
* **Available hooks**
  * [checkstyle-jar](checkstyle-jar.md)
  * [end-of-file](end-of-file.md)
  * [trailing-whitespaces](trailing-whitespaces.md)

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

#### Arguments

* `--jar` path to the Checkstyle JAR file. If not specified, looks for `checkstyle-9.0-all.jar` in project directory.

#### Example

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: checkstyle-jar
      args: [ '--jar=/path/to/checkstyle.jar' ]
```

### `end-of-file`

Makes sure files end in a newline and only a newline.

#### Arguments

* `--fix` if used, hook will correct invalid files in-place.

#### Example

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: end-of-file
      args: [ '--fix' ]
```

### `trailing-whitespaces`

Ensures there's no line trailing whitespaces.

#### Arguments

* `--jar` path to the Checkstyle JAR file. If not specified, looks for `checkstyle-9.0-all.jar` in project directory.

#### Example

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: checkstyle-jar
      args: [ '--jar=/path/to/checkstyle.jar' ]
```

## License ##

* Written and copyrighted &copy;2021 by Marcin Orlowski <mail (#) marcinorlowski (.) com>
* This is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT).
