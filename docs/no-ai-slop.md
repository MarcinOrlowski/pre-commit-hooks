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
  - [commit-msg](commit-msg.md)
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

### Quotation marks and primes ###

| Character | Code point | Name                                  |
|-----------|------------|---------------------------------------|
| `“`       | `U+201C`   | LEFT DOUBLE QUOTATION MARK            |
| `”`       | `U+201D`   | RIGHT DOUBLE QUOTATION MARK           |
| `„`       | `U+201E`   | DOUBLE LOW-9 QUOTATION MARK           |
| `‟`       | `U+201F`   | DOUBLE HIGH-REVERSED-9 QUOTATION MARK |
| `‘`       | `U+2018`   | LEFT SINGLE QUOTATION MARK            |
| `’`       | `U+2019`   | RIGHT SINGLE QUOTATION MARK           |
| `‚`       | `U+201A`   | SINGLE LOW-9 QUOTATION MARK           |
| `‛`       | `U+201B`   | SINGLE HIGH-REVERSED-9 QUOTATION MARK |
| `′`       | `U+2032`   | PRIME                                 |
| `″`       | `U+2033`   | DOUBLE PRIME                          |

### Dashes, hyphens and their lookalikes ###

| Character | Code point | Name                |
|-----------|------------|---------------------|
| `—`       | `U+2014`   | EM DASH             |
| `–`       | `U+2013`   | EN DASH             |
| `‐`       | `U+2010`   | HYPHEN              |
| `‑`       | `U+2011`   | NON-BREAKING HYPHEN |
| `‒`       | `U+2012`   | FIGURE DASH         |
| `―`       | `U+2015`   | HORIZONTAL BAR      |
| `−`       | `U+2212`   | MINUS SIGN          |

### Spaces ###

Not rendered in the table below, as they are indistinguishable from a regular space (`U+0020`,
which is of course allowed):

| Code point | Name                      |
|------------|---------------------------|
| `U+00A0`   | NO-BREAK SPACE            |
| `U+2002`   | EN SPACE                  |
| `U+2003`   | EM SPACE                  |
| `U+2007`   | FIGURE SPACE              |
| `U+2009`   | THIN SPACE                |
| `U+202F`   | NARROW NO-BREAK SPACE     |
| `U+205F`   | MEDIUM MATHEMATICAL SPACE |
| `U+3000`   | IDEOGRAPHIC SPACE         |

### Invisible and bidirectional format characters ###

These render as nothing at all. The bidirectional controls are the "Trojan Source" attack vector
([CVE-2021-42574](https://nvd.nist.gov/vuln/detail/CVE-2021-42574)): they can make source code
display in an order different from the one the compiler sees.

| Code point | Name                        |
|------------|-----------------------------|
| `U+00AD`   | SOFT HYPHEN                 |
| `U+200B`   | ZERO WIDTH SPACE            |
| `U+200C`   | ZERO WIDTH NON-JOINER       |
| `U+2060`   | WORD JOINER                 |
| `U+FEFF`   | ZERO WIDTH NO-BREAK SPACE   |
| `U+202A`   | LEFT-TO-RIGHT EMBEDDING     |
| `U+202B`   | RIGHT-TO-LEFT EMBEDDING     |
| `U+202C`   | POP DIRECTIONAL FORMATTING  |
| `U+202D`   | LEFT-TO-RIGHT OVERRIDE      |
| `U+202E`   | RIGHT-TO-LEFT OVERRIDE      |
| `U+2066`   | LEFT-TO-RIGHT ISOLATE       |
| `U+2067`   | RIGHT-TO-LEFT ISOLATE       |
| `U+2068`   | FIRST STRONG ISOLATE        |
| `U+2069`   | POP DIRECTIONAL ISOLATE     |

### Deliberately allowed ###

| Character | Code point | Name                                | Why                                  |
|-----------|------------|-------------------------------------|--------------------------------------|
| `…`       | `U+2026`   | HORIZONTAL ELLIPSIS                 | too common in legitimate prose       |
| `«`       | `U+00AB`   | LEFT-POINTING DOUBLE ANGLE QUOTE    | regular quotes in i.e. FR/PL/DE text |
| `»`       | `U+00BB`   | RIGHT-POINTING DOUBLE ANGLE QUOTE   | as above                             |
| n/a       | `U+200D`   | ZERO WIDTH JOINER                   | required by emoji sequences          |

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
