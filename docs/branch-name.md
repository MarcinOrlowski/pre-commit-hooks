![pre-commit-hooks logo](../artwork/logo.png)

Handy Git hooks to integrate with [pre-commit](http://pre-commit.com/) framework.

---

<!--TOC-->

* [« Main README](../README.md)

- [Configure pre-commit](../README.md#configure-pre-commit)
- [Two ways to invoke pre-commit](../README.md#two-ways-to-invoke-pre-commit)
- **Available hooks**
  - **branch-name**
  - [checkstyle-jar](checkstyle-jar.md)
  - [end-of-file](end-of-file.md)
  - [trailing-whitespaces](trailing-whitespaces.md)

<!--TOC-->

## Summary ##

* Hook ID: `branch-name`

## Description ##

Verifies that the current Git branch name matches a required regular expression. Intended to be
wired up to the `pre-push` stage so that attempts to push a branch whose name violates the
project's naming convention are blocked before they reach the remote.

`pre-commit` has no first-class knowledge of pull requests, but enforcing the check at push time
effectively blocks most PRs from being opened against a remote branch that was never allowed to
exist there in the first place.

The hook exits with code `0` when the branch name passes, `1` when it fails, and `10` when the
`--pattern` argument is not a valid regular expression. If `HEAD` is detached (no branch), the
hook passes and prints a short note.

## Configuration ##

The hook is configured with a small YAML file checked into your repository. By default it looks
for `.branch-name.yaml` in the repository root, but the path can be changed with `--config`.

### Config file schema ###

```yaml
# .branch-name.yaml

# Regular expression the branch name must fully match (re.fullmatch).
# Required unless --pattern is passed on the command line.
pattern: '\d+-[a-z0-9-]+'

# List of branch names that bypass the pattern check. Typically used
# for long-lived branches such as master or dev that were created
# before the convention existed.
allow:
  - master
  - dev
```

### Arguments ###

* `-c PATH`, `--config PATH` — path to the YAML config file. Defaults to `.branch-name.yaml`. It
  is not an error for the default file to be missing; a non-default path must exist.
* `-p PATTERN`, `--pattern PATTERN` — regular expression override. When provided, it takes
  precedence over the `pattern` value in the config file. Useful for one-off usage without a
  config file at all.

## Examples ##

### Minimum setup ###

`.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: branch-name
      stages: [ pre-push ]
```

`.branch-name.yaml` (committed to the repo root):

```yaml
pattern: '\d+-[a-z0-9-]+'
allow:
  - master
  - dev
```

### Adding more branches to the whitelist ###

Edit `.branch-name.yaml` and extend the `allow` list — one YAML list item per branch. No
separators, no CLI arguments to juggle:

```yaml
pattern: '\d+-[a-z0-9-]+'
allow:
  - master
  - dev
  - release
  - staging
  - hotfix
```

### Custom config file location ###

If you prefer to keep the config elsewhere (e.g. under a `config/` directory), point
`--config` at it:

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: branch-name
      stages: [ pre-push ]
      args: [ '--config=config/branch-name.yaml' ]
```

### Without a config file ###

For trivial projects you can skip the config file entirely and pass the pattern on the command
line. No `allow` list is available in this mode:

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: branch-name
      stages: [ pre-push ]
      args: [ '--pattern=\d+-[a-z0-9-]+' ]
```

### Enabling the `pre-push` stage ###

The hook only runs at the `pre-push` stage, so the `pre-push` hook type must be installed in the
consumer repository once (in addition to the default `pre-commit` type):

```bash
$ pre-commit install --hook-type pre-push
```

### What users see ###

On a valid branch (e.g. `42-add-login`) the hook exits `0` silently and the push proceeds. On an
invalid branch (e.g. `my-experiment`) the push is aborted with:

```
Branch name "my-experiment" does not match required pattern: \d+-[a-z0-9-]+
Allowed exceptions: master, dev
```

## Exit codes ##

* `0` — branch name matches the pattern, or is in the `allow` list, or HEAD is detached.
* `1` — branch name does not match and is not whitelisted.
* `10` — configuration error (missing config file at a non-default path, invalid YAML, invalid
  regex, no pattern at all, wrong types in the config).

