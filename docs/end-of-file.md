![pre-commit-hooks logo](../artwork/logo.png)

Handy Git hooks to integrate with [pre-commit](http://pre-commit.com/) framework.

---

<!--TOC-->

- [Configure pre-commit](#configure-pre-commit)
- [Two ways to invoke pre-commit](#two-ways-to-invoke-pre-commit)
- [Available hooks](#available-hooks)
  - [`checkstyle-jar`](#checkstyle-jar)
  - [`end-of-file`](#end-of-file)
  - [`trailing-whitespaces`](#trailing-whitespaces)
- [License](#license)

<!--TOC-->

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

