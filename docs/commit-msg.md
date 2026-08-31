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
  - **commit-msg**
  - [composer-lock-in-sync](composer-lock-in-sync.md)
  - [end-of-file](end-of-file.md)
  - [no-ai-slop](no-ai-slop.md)
  - [trailing-whitespaces](trailing-whitespaces.md)

<!--TOC-->

## Summary ##

* Hook ID: `commit-msg`

## Description ##

Enforces the shape of the commit message: how many lines it may span and how long each of these
lines may be. By default only a single line (the subject) is allowed, and no line may be longer
than 100 characters.

The hook runs at the `commit-msg` stage, so a message violating the limits aborts the commit
before it is created. The rejected message is not lost - Git keeps it in `.git/COMMIT_EDITMSG`,
so `git commit -e --file=.git/COMMIT_EDITMSG` brings it back up for editing.

### What counts as a line ###

The hook inspects the message the way Git will actually store it, not the raw contents of the
message file. Before the limits are applied:

* everything from the "scissors" line (`# ------------------------ >8 ------...`) down is
  dropped, so the diff appended by `git commit --verbose` is not counted,
* comment lines (lines starting with `core.commentChar`, `#` unless configured otherwise) are
  removed,
* trailing whitespace is stripped from every line,
* runs of empty lines are collapsed into a single empty line, and leading/trailing empty lines
  are removed.

An empty message passes - Git aborts such a commit on its own.

Note that with the default `--max-lines=1` the customary "subject, blank line, body" layout is
rejected, as that message spans three lines. Raise the limit if you want to allow a body.

## Configuration ##

### Arguments ###

* `-n COUNT`, `--max-lines COUNT` - maximum number of lines the message may span. Defaults to
  `1`. Use `0` to disable the check.
* `-w COUNT`, `--max-length COUNT` - maximum length of a single line, in characters. Defaults to
  `100`. Use `0` to disable the check.

## Examples ##

### Minimum setup ###

`.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: commit-msg
      stages: [ commit-msg ]
```

### Allowing a message body ###

Allow a subject, a blank line and up to eight lines of body, wrapped at the traditional 72
characters:

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: commit-msg
      stages: [ commit-msg ]
      args: [ '--max-lines=10', '--max-length=72' ]
```

### Checking line length only ###

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: commit-msg
      stages: [ commit-msg ]
      args: [ '--max-lines=0', '--max-length=100' ]
```

### Enabling the `commit-msg` stage ###

The hook only runs at the `commit-msg` stage, so the `commit-msg` hook type must be installed in
the consumer repository once (in addition to the default `pre-commit` type):

```bash
$ pre-commit install --hook-type commit-msg
```

### What users see ###

With the defaults in place, committing a multi-line message aborts the commit with:

```
Commit message spans 3 lines, while at most 1 is allowed.
```

and an over-long subject with:

```
Commit message line 1 is 118 characters long, exceeding the limit of 100.
  | Refactored the whole thing so that it no longer explodes when the configuration file happens to be missing
```

## Exit codes ##

* `0` - the message fits within both limits (or is empty).
* `1` - the message has too many lines, or at least one line is too long.
* `10` - configuration error (a limit that is not a non-negative integer, an unreadable message
  file, or the hook not being run at the `commit-msg` stage).
