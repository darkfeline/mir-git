# Copyright (C) 2017 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import contextlib
import io
import subprocess
from unittest import mock

import pytest

from mir import git


def test_git_default():
    with pytest.raises(NotImplementedError):
        git.git(object(), ['foobar'])


@mock.patch('subprocess.run')
def test_git_str(run):
    git.git('foo', ['foobar'])
    run.assert_called_once_with(
        ['git', '--git-dir', 'foo/.git', '--work-tree', 'foo', 'foobar'])


@mock.patch.dict('os.environ', HOME='/home/git')
@mock.patch('subprocess.run')
def test_git_str_expanduser(run):
    git.git('~/foo', ['foobar'])
    run.assert_called_once_with(
        ['git', '--git-dir', '/home/git/foo/.git',
         '--work-tree', '/home/git/foo', 'foobar'])


def test_git_status(gitdir):
    result = git.git(gitdir, ['status'])
    assert result.returncode == 0


def test_git_has_unpushed_changes(gitdir):
    subprocess.run(['git', 'branch', '-t', 'slave'])
    subprocess.run(['git', 'checkout', 'slave'])
    (gitdir / 'bar').touch()
    subprocess.run(['git', 'add', 'bar'])
    subprocess.run(['git', 'commit', '-m', 'bar'])
    assert git.has_unpushed_changes(gitdir)


def test_git_has_unpushed_changes_false(gitdir):
    assert not git.has_unpushed_changes(gitdir)


def test_git_has_unstaged_changes(gitdir):
    (gitdir / 'foo').write_text('bar\n')
    assert git.has_unstaged_changes(gitdir)


def test_git_has_unstaged_changes_false(gitdir):
    assert not git.has_unstaged_changes(gitdir)


def test_git_has_staged_changes(gitdir):
    (gitdir / 'foo').write_text('bar\n')
    subprocess.run(['git', 'add', 'foo'])
    assert git.has_staged_changes(gitdir)


def test_git_has_staged_changes_false(gitdir):
    assert not git.has_staged_changes(gitdir)


def test_git_get_current_branch(gitdir):
    assert git.get_current_branch(gitdir) == 'master'


def test_git_save_branch(gitdir):
    subprocess.run(['git', 'branch', 'slave'])
    with git.save_branch(gitdir):
        subprocess.run(['git', 'checkout', 'slave'])
    branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                            stdout=subprocess.PIPE).stdout.decode().rstrip()
    assert branch == 'master'


def test_git_save_branch_should_be_quiet(gitdir):
    subprocess.run(['git', 'branch', 'slave'])
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        with git.save_branch(gitdir):
            subprocess.run(['git', 'checkout', 'slave'])
    assert f.getvalue() == ''


def test_git_save_branch_should_raise_when_restore_fails(gitdir):
    subprocess.run(['git', 'branch', 'slave'])
    with pytest.raises(subprocess.CalledProcessError):
        with git.save_branch(gitdir):
            subprocess.run(['git', 'checkout', 'slave'])
            subprocess.run(['git', 'branch', '-d', 'master'])
