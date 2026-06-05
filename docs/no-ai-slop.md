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
  - **no-ai-slop**
  - [trailing-whitespaces](trailing-whitespaces.md)

<!--TOC-->

## Summary ##

* Hook ID: `no-ai-slop`

## Description ##

Scans modified text files for "forbidden" typographic characters — the kind most commonly
introduced by AI text generators when they rewrite plain ASCII into "prettier" Unicode. When any
forbidden character is found the hook fails the commit and reports the offending file, line,
column, code point and Unicode name. There is **no autofix**: the hook only detects.

The default forbidden set is:

| Character | Code point | Name                       |
|-----------|------------|----------------------------|
| `—`       | `U+2014`   | EM DASH                    |
| `–`       | `U+2013`   | EN DASH                    |
| `“`       | `U+201C`   | LEFT DOUBLE QUOTATION MARK |
| `”`       | `U+201D`   | RIGHT DOUBLE QUOTATION MARK|
| `‘`       | `U+2018`   | LEFT SINGLE QUOTATION MARK |
| `’`       | `U+2019`   | RIGHT SINGLE QUOTATION MARK|
| ` `       | `U+00A0`   | NO-BREAK SPACE             |
| `​`        | `U+200B`   | ZERO WIDTH SPACE           |

The ellipsis character (`…`, `U+2026`) is **not** forbidden by default.

The hook's manifest restricts it to `types: [text]`, so binary files are skipped by pre-commit.
A file that is staged but not valid UTF-8 is skipped with a `[SKIP]` notice rather than failing.

## Arguments ##

* `--chars CHARS` — the set of characters to forbid. Supplying this **replaces** the built-in
  default set, so include every character you want to block. An empty value is rejected with
  exit code `10`.

## Examples ##

### Default set ###

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: no-ai-slop
      # We do not want binary files to be scanned
      exclude_types: [ 'xml','png','jpeg','svg' ]
```

### Custom set ###

Forbid only em and en dashes:

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: no-ai-slop
      args: [ '--chars=—–' ]
```

## What users see ##

On a clean state the hook exits silently with code `0`. When a forbidden character is found:

```
README.md:12:34: forbidden character U+2014 (EM DASH)
docs/intro.md:3:8: forbidden character U+201C (LEFT DOUBLE QUOTATION MARK)
```

The line and column are 1-based. The commit is blocked until the offending characters are removed.

## Exit codes ##

* `0` — no forbidden characters found.
* `1` — at least one forbidden character found (or a file could not be read).
* `10` — invalid `--chars` value (empty set).
