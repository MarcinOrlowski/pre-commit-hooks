![pre-commit-hooks logo](../artwork/logo.png)

Handy Git hooks to integrate with [pre-commit](http://pre-commit.com/) framework.

---

<!--TOC-->

## Table of contents ##

* [« Main README](../README.md)
* [« Hooks table of contents](README.md)
  * [checkstyle-jar](checkstyle-jar.md)
  * [end-of-file](end-of-file.md)
  * [trailing-whitespaces](trailing-whitespaces.md)

<!--TOC-->

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

