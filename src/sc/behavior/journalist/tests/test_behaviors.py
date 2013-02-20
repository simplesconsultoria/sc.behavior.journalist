# -*- coding: utf-8 -*-

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from sc.behavior.journalist.behaviors import IJournalist
from sc.behavior.journalist.testing import INTEGRATION_TESTING
from zope.component import queryUtility

import unittest2 as unittest


class MockJournalist(object):
    email = ""
    resume = ""


class IContactInfoTest(unittest.TestCase):

    name = 'sc.behavior.journalist.behaviors.IJournalist'

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.pt = self.portal.portal_types
        self.pc = self.portal['portal_personcatalog']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        behaviors = []
        behaviors.append(self.name)
        fti = queryUtility(IDexterityFTI, name='Person')
        fti.behaviors = tuple(behaviors)

    def test_registration(self):
        registration = queryUtility(IBehavior, name=self.name)
        self.assertIsNotNone(registration)

    def test_behavior_in_person(self):
        # XXX: I don't think this is useful
        fti = queryUtility(IDexterityFTI, name='Person')
        behaviors = fti.behaviors
        self.assertIn(self.name, behaviors)

    def test_adapt_content(self):
        self.folder.invokeFactory('Person', 'p1')
        p1 = self.folder['p1']
        journalist = IJournalist(p1)
        self.assertIsNotNone(journalist)

    def test_email(self):
        self.folder.invokeFactory('Person', 'user1')
        user1 = self.folder['user1']
        journalist = IJournalist(user1)
        journalist.email = "email@example.com"
        self.assertEqual(journalist.email, "email@example.com")

    def test_resume(self):
        self.folder.invokeFactory('Person', 'user1')
        user1 = self.folder['user1']
        journalist = IJournalist(user1)
        journalist.resume = u"somebody, somewhere"
        self.assertEqual(journalist.resume, u"somebody, somewhere")
