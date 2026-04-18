![pre-commit-hooks logo](artwork/logo.png)

Handy Git hooks to integrate with [pre-commit](http://pre-commit.com/) framework.

---

<!--TOC-->

- [Configure pre-commit](#configure-pre-commit)
- [Two ways to invoke pre-commit](#two-ways-to-invoke-pre-commit)
- **Available hooks**
  * [branch-name](docs/branch-name.md) — verifies the current Git branch name matches a required regular expression (runs at `pre-push`).
  * [checkstyle-jar](docs/checkstyle-jar.md) — runs the Checkstyle JAR against modified Java files.
  * [end-of-file](docs/end-of-file.md) — ensures each file is empty or ends with exactly one newline.
  * [trailing-whitespaces](docs/trailing-whitespaces.md) — detects (and optionally strips) trailing whitespace.
- [License](#license)

<!--TOC-->

---

## Configure pre-commit

**NOTE:** hooks require Python 3.

Add `.pre-commit-config.yaml` config file to in your project:

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: 1.0.0  # or any specific git tag
  hooks:
    - id: branch-name
      stages: [ pre-push ]
      # args: [ '--config=.branch-name.yaml' ]
    - id: checkstyle-jar
      # args: [ '--jar=/path/to/checkstyle.jar' ]
    - id: end-of-file
      # exclude_types: ['xml','png','jpeg','svg']
      # args: [ '--fix=yes' ]
    - id: trailing-whitespaces
      # exclude_types: ['xml','png','jpeg','svg']
      # args: [ '--fix=no' ]
```

---

## Two ways to invoke pre-commit

If you want to invoke the checks as a git pre-commit hook, run:

```bash
$ pre-commit install
```

If you want to run the checks on-demand (outside of git hooks), run:

```bash
$ pre-commit run --all-files --verbose
```

To try your hooks with all the files present.

> **NOTE:** This will apply your hooks too **ALL** the files, which
> in case of using modifying hooks might not what you really want!

## License ##

* Written and copyrighted &copy;2021-2026 by Marcin Orlowski <mail (#) marcinorlowski (.) com>
* This is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT)
