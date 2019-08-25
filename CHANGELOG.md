# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to *access-modifiers* will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- The line "## <square-bracket>Unreleased</square-bracket>" is replaced by the ci/release.py script with the new release version and release date. -->

## [0.2.0] - [2019-08-26]

### Added

- Allow for static private methods. Closes [#4](https://github.com/fniessink/access-modifiers/issues/4).

## [0.1.4] - [2019-08-25]

### Fixed

- Make the access modifiers work when called from a dict comprehension, list comprehension, lambda, or other code block that gets its own frame. Fixes [#5](https://github.com/fniessink/access-modifiers/issues/5).

## [0.1.3] - [2019-08-24]

### Fixed

- Another small performance improvement by using `sys._getframe()` instead of the inspect module to get the caller's frame. Fixes [#2](https://github.com/fniessink/access-modifiers/issues/2).

## [0.1.2] - [2019-08-24]

### Fixed

- Improved performance. Creating methods with an access modifier is now a factor 2-3 slower than without access modifier. Invoking methods with an access modifier is a factor 10-20 slower than methods without access modifier. Fixes [#2](https://github.com/fniessink/access-modifiers/issues/2).

### Added

- Added performance tests. Closes [#1](https://github.com/fniessink/access-modifiers/issues/1).

## [0.1.1] - [2019-08-24]

### Fixed

- Added PyPI installation instructions.

## [0.1.0] - [2019-08-24]

### Added

- Initial release. 
