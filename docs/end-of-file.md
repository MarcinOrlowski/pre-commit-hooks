![pre-commit-hooks logo](../artwork/logo.png)

Handy Git hooks to integrate with [pre-commit](http://pre-commit.com/) framework.

---

<!--TOC-->

- [Configure pre-commit](#configure-pre-commit)
- [Two ways to invoke pre-commit](#two-ways-to-invoke-pre-commit)
- [Available hooks](#available-hooks)
  - [`checkstyle-jar`](#checkstyle-jar)
  - **end-of-file**
    * [Summary](#summary)
    * [Description](#description)
    * [Arguments](#arguments)
    * [Examples](#examples)
  - [`trailing-whitespaces`](#trailing-whitespaces)
- [License](#license)

<!--TOC-->

## Summary ##

* Hook ID: `end-of-file`

## Description ##

Makes sure files end in a newline and only a newline.

## Arguments ##

* `--fix` if used, hook will correct invalid files in-place. Supported values are `yes` and `no` (default).

## Examples ##

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: end-of-file
      args: [ '--fix=yes' ]
```

