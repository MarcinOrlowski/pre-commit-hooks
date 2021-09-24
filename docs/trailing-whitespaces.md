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
- [License](#license)

<!--TOC-->

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
