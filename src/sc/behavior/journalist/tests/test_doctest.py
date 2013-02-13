#-*- coding: utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from sc.behavior.journalist import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/owner_edit.txt',
                                     package='sc.behavior.journalist'),
                layer=FUNCTIONAL_TESTING),
        ])
    return suite
