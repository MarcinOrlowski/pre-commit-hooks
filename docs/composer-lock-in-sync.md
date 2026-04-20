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
  - **composer-lock-in-sync**
  - [end-of-file](end-of-file.md)
  - [trailing-whitespaces](trailing-whitespaces.md)

<!--TOC-->

## Summary ##

* Hook ID: `composer-lock-in-sync`

## Description ##

Verifies that [Composer](https://getcomposer.org/)'s `composer.lock` is not older than
`composer.json`. The moment `composer.json` is edited (a dependency added, a version bumped, …)
`composer.lock` must be regenerated to stay consistent, and this hook blocks the commit until
that happens.

The hook is a **no-op** when either `composer.json` or `composer.lock` is missing, so it is
safe to enable repo-wide — it simply does nothing in projects that do not use Composer.

Detection is based on the files' modification times (`mtime`). The hook's manifest is wired to
fire only when one of the two files is staged, so it will not run on unrelated commits.

## Arguments ##

* `--path PATH` — directory containing `composer.json` and `composer.lock`. Defaults to the
  current working directory, which is what `pre-commit` hands the hook. Override this only if
  the Composer project lives in a subdirectory of the repository (for example a monorepo).

## Examples ##

### Standard project ###

Composer files live in the repository root — no arguments needed:

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: composer-lock-in-sync
```

### Composer in a subdirectory ###

If your PHP project sits under `backend/`, tell the hook where to look:

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: composer-lock-in-sync
      args: [ '--path=backend' ]
      files: '^backend/(composer\.json|composer\.lock)$'
```

(The `files:` override replaces the hook's built-in regex so it still fires on edits to the
subdirectory copies of the files.)

## What users see ##

On a valid state the hook exits silently with code `0`. When `composer.lock` is older than
`composer.json`:

```
composer.lock is older than composer.json and must be regenerated.
Run one of:
  composer update --lock
  composer update --lock --ignore-platform-reqs
```

The commit is blocked. After running either command the `mtime` of `composer.lock` is refreshed
and the hook passes.

## Exit codes ##

* `0` — both files present and in sync, or one/both files missing (nothing to check).
* `1` — `composer.lock` is older than `composer.json`.
