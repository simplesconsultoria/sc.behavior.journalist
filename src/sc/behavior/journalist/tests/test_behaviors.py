# -*- coding: utf-8 -*-

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from sc.behavior.journalist.behaviors import IJournalist
from sc.behavior.journalist.testing import INTEGRATION_TESTING
from zope.component import queryUtility

import unittest


class IContactInfoTest(unittest.TestCase):

    layer = INTEGRATION_TESTING
    behavior_name = 'sc.behavior.journalist.behaviors.IJournalist'

    def setUp(self):
        self.portal = self.layer['portal']
        self.pt = self.portal.portal_types
        self.pc = self.portal['portal_personcatalog']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        behaviors = []
        behaviors.append(self.behavior_name)
        fti = queryUtility(IDexterityFTI, name='Person')
        fti.behaviors = tuple(behaviors)

    def test_registration(self):
        registration = queryUtility(IBehavior, name=self.behavior_name)
        self.assertIsNotNone(registration)

    def test_behavior_in_person(self):
        fti = queryUtility(IDexterityFTI, name='Person')
        behaviors = fti.behaviors
        self.assertIn(self.behavior_name, behaviors)

    def test_adapt_content(self):
        self.folder.invokeFactory('Person', 'p1')
        p1 = self.folder['p1']
        journalist = IJournalist(p1)
        self.assertIsNotNone(journalist)

    def test_email(self):
        self.folder.invokeFactory('Person', 'user1')
        user1 = self.folder['user1']
        journalist = IJournalist(user1)
        self.assertEqual(journalist.email, u"")
        journalist.email = u"email@example.com"
        self.assertEqual(journalist.email, u"email@example.com")

    def test_resume(self):
        self.folder.invokeFactory('Person', 'user1')
        user1 = self.folder['user1']
        journalist = IJournalist(user1)
        self.assertEqual(journalist.resume, u"")
        journalist.resume = u"somebody, somewhere"
        self.assertEqual(journalist.resume, u"somebody, somewhere")

    def test_signature(self):
        self.folder.invokeFactory('Person', 'user1')
        user1 = self.folder['user1']
        journalist = IJournalist(user1)
        self.assertEqual(journalist.signature, u"")
        journalist.signature = u"John Doe, of the Plone Foundation"
        self.assertEqual(
            journalist.signature, u"John Doe, of the Plone Foundation")
