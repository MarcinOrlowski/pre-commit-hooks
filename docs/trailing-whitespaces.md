![pre-commit-hooks logo](../artwork/logo.png)

Handy Git hooks to integrate with [pre-commit](http://pre-commit.com/) framework.

---

<!--TOC-->

- [Configure pre-commit](#configure-pre-commit)
- [Two ways to invoke pre-commit](#two-ways-to-invoke-pre-commit)
- [Available hooks](#available-hooks)
  - [checkstyle-jar](#checkstyle-jar)
  - [end-of-file](#end-of-file)
  - **trailing-whitespaces**
    * [Summary](#summary)
    * [Description](#description)
    * [Arguments](#arguments)
    * [Examples](#examples)
- [License](#license)

<!--TOC-->

## Summary ##

* Hook ID: `trailing-whitespaces`

## Description ##

Ensures there's no line trailing whitespaces.

## Arguments ##

* `--jar` path to the Checkstyle JAR file. If not specified, looks for `checkstyle-9.0-all.jar` in project directory.

## Examples ##

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: trailing-whitespaces
      args: [ '--fix' ]
```
