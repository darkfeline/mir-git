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
