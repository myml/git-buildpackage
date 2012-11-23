# vim: set fileencoding=utf-8 :

"""Test L{gbp.pq}"""

import os
import unittest

import gbp.scripts.common.pq
import gbp.patch_series
import tests.testutils as testutils

class TestApplyAndCommit(testutils.DebianGitTestRepo):
    """Test L{gbp.pq}'s apply_and_commit"""

    def setUp(self):
        testutils.DebianGitTestRepo.setUp(self)
        self.add_file('bar')

    def test_apply_and_commit_patch(self):
        """Test applying a single patch"""
        patch = gbp.patch_series.Patch(
            os.path.join(os.path.abspath(os.path.curdir),
                         'tests/data/foo.patch'))
        
        gbp.scripts.common.pq.apply_and_commit_patch(self.repo, patch)
        self.assertIn('foo', self.repo.list_files())

    @unittest.skipIf(not os.path.exists('/usr/bin/dpkg'), 'Dpkg not found')
    def test_debian_missing_author(self):
        """
        Check if we parse the author from debian control
        if it's missing.
        """
        patch = gbp.patch_series.Patch(
            os.path.join(os.path.abspath(os.path.curdir),
                         'tests/data/foo.patch'))

        # Overwrite data parsed from patch:
        patch.author
        patch.info['author'] = None
        patch.info['email'] = None

        # Fake a control file
        self.add_file("debian/control",
                      "Maintainer: Guido Günther <gg@godiug.net>")
        
        gbp.scripts.common.pq.apply_and_commit_patch(self.repo, patch)
        info = self.repo.get_commit_info('HEAD')
        self.assertEqual(info['author'].email, 'gg@godiug.net')
        self.assertIn('foo', self.repo.list_files())


        



