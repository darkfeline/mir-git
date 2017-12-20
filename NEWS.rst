mir.git Release Notes
=====================

This project uses `semantic versioning <http://semver.org/>`_.

2.0.0 (2017-12-20)
------------------

Added
^^^^^

- `save_worktree_and_branch()` context manager.
- `process_env()` function.
- `gitdir()` generic function.
- `worktree()` generic function.
- `GitEnvInterface` for dynamic checking of interface.

Changed
^^^^^^^

- `GitEnv` is now a named tuple.
- `git()` is no longer a generic function.
- `save_worktree()` no longer saves branch.

Fixed
^^^^^

- Work around bug in `git-stash`.

1.2.1 (2017-09-12)
------------------

Fixed
^^^^^

- Make `save_worktree()` raise an exception if any commands fail.

1.2.0 (2017-07-13)
------------------

Added
^^^^^

- Added `get_branches()`.
- Added `default_encoding`.

1.1.1 (2017-06-22)
------------------

Fixed
^^^^^

- Fixed `save_wortree()` printing to stdout/stderr.
- Use `stash create` to make `save_wortree()` more robust.

1.1.0 (2017-06-22)
------------------

Added
^^^^^

- `get_current_branch()`
- `save_branch()`
- `save_worktree()`

1.0.1 (2017-06-17)
------------------

Changed
^^^^^^^

- Fixed various links.
- `git()` now works with bytes and PathLike.

1.0.0 (2017-04-21)
------------------

Initial release.
