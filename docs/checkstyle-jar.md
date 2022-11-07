![pre-commit-hooks logo](../artwork/logo.png)

Handy Git hooks to integrate with [pre-commit](http://pre-commit.com/) framework.

---

<!--TOC-->

## Table of contents ##

* [« Main README](../README.md)

- [Configure pre-commit](../README.md#configure-pre-commit)
- [Two ways to invoke pre-commit](../README.md#two-ways-to-invoke-pre-commit)
- **Available hooks**
  * **checkstyle-jar**
  * [end-of-file](end-of-file.md)
  * [trailing-whitespaces](trailing-whitespaces.md)

<!--TOC-->

---

## Summary ##

* Hook ID: `checkstyle-jar`
* Depends on: Java, [CheckStyle JAR](https://checkstyle.org/)

## Description ##

Uses [CheckStyle](https://checkstyle.org/) linter against Java source codes. Contrary to other
implementations this one **requires** CheckStyle JAR file (can be downloaded from
official [release section](https://github.com/checkstyle/checkstyle/releases/)) to be given, instead
of using system-wide available application. This hook expects `java` binary to be in `$PATH`.

Note, you must configure this hook before use. JAR file can be downloaded from their official
[Checkstyle releases](https://github.com/checkstyle/checkstyle/releases/) section.

## Arguments ##

* `--jar-url` full URL to downloadable Checkstyle JAR file. If specified, and there's no cached JAR
  file found, the JAR file will be automatically downloaded and cached locally. If not give, will
  try to download recent version automatically.
* `--jar` path to the Checkstyle JAR file. If not specified, looks for `checkstyle-10.4-all.jar` in
  project directory.
* `--cache` path to cache directory where downloaded JAR should be stored (defaults
  to `~/.cache/pre-commit/`).
* `--config` path to Checkstyle config file to use. Alternatively you can use `/google_checks.xml`
  and `/sun_checks.xml` to use Checkstyle's built-in styles.

## Examples ##

```yaml
- repo: https://github.com/MarcinOrlowski/pre-commit-hooks
  rev: main
  hooks:
    - id: checkstyle-jar
      args: [ '--jar=/path/to/checkstyle.jar' ]
```

