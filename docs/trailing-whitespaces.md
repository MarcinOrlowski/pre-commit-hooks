![pre-commit-hooks logo](../artwork/logo.png)

Handy Git hooks to integrate with [pre-commit](http://pre-commit.com/) framework.

---

<!--TOC-->

* [« Main README](../README.md)

- [Configure pre-commit](../README.md#configure-pre-commit)
- [Two ways to invoke pre-commit](../README.md#two-ways-to-invoke-pre-commit)
- **Available hooks**
  - [branch-name](branch-name.md)
  - [checkstyle-jar](checkstyle-jar.md)
  - [composer-lock-in-sync](composer-lock-in-sync.md)
  - [end-of-file](end-of-file.md)
  - **trailing-whitespaces**

<!--TOC-->

## Summary ##

* Hook ID: `trailing-whitespaces`

## Description ##

Ensures there's no line trailing whitespaces.

## Arguments ##

* `--fix` if used, hook will correct invalid files in-place. Supported values are `yes` and `no` (
  default).

## Examples ##

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: trailing-whitespaces
      # We do not want binary files to be touched
      exclude_types: [ 'xml','png','jpeg','svg' ]
      args: [ '--fix=yes' ]
```
