![pre-commit-hooks logo](artwork/logo.png)

Handy Git hooks to integrate with [pre-commit](http://pre-commit.com/) framework.

---

# Changelog #

* v1.3.1 (2022-11-07)
  * Updated docs to include `exclude_types` example (i.f. for binaries).
  * Bumped default version of Checkstyle to 10.4


* v1.3.0 (2021-09-29)
  * Added "safe save" mode to `trailing-whitespace` hook. 


* v1.2.2 (2021-09-28)
  * Changed the wat `trailing-whitespaces` handles files it fixes.


* v1.2.1 (2021-09-25)
  * Fixed `checkstyle-jar` argument handling.


* v1.2.0 (2021-09-24)
  * `checkstyle-jar` now can automatically download and cache JAR file.
  * `checkstyle-jar` accepts `--config` argument now.
  * `end-of-file` and `trailing-whitespaces`'s `--fix` now requires "yes/no" argument.


* v1.1.0 (2021-09-23)
  * Added new hooks:
    * `trailing-whitespaces`
    * `end-of-file`


* v1.0.0 (2021-09-23)
  * Initial release.
