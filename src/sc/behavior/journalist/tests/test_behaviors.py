# -*- coding: utf-8 -*-


import unittest2 as unittest

#from five import grok

from zope.component import queryUtility
from zope.interface import Invalid

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.behavior.interfaces import IBehavior

#from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI

#from s17.person.content.person import Person
#from s17.person.content.person import IPerson

#from s17.person.behaviors.contact import IContactInfo

#from s17.person.behaviors.user import INameFromUserName
#from s17.person.behaviors.user import IPloneUser

from sc.behavior.journalist import IJournalist

from  sc.behavior.journalist import INTEGRATION_TESTING


class MockJournalist(object):
    email = ""
    biography = ""

class IContactInfoTest(unittest.TestCase):

    name = 'sc.behavior.IJournalist'

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
        fti = queryUtility(IDexterityFTI,
                           name='Person')
        fti.behaviors = tuple(behaviors)

    def test_registration(self):
        registration = queryUtility(IBehavior, name=self.name)
        self.assertNotEquals(None, registration)

    def test_set_in_person(self):
        fti = queryUtility(IDexterityFTI,
                           name='Person')
        behaviors = fti.behaviors
        self.assertTrue(self.name in behaviors)

    def test_adapt_content(self):
        self.folder.invokeFactory('Person', 'p1')
        p1 = self.folder['p1']
        adapter = IJournalist(p1)
        self.assertNotEquals(None, adapter)

    def test_email(self):
        self.folder.invokeFactory('Person', 'user1')
        user1 = self.folder['user1']
        adapter = IJournalist(user1)
        adapter.email = "email@example.com"
        self.assertEquals(adapter.email,"email@example.com" )

    def test_valid_emails(self):
        data = MockJournalist()
        data.email = "email@example.com"
        try:
            IJournalist.validateInvariants(data)
        except Invalid:
            self.fail()

    def test_invalid_emails(self):
        data = MockJournalist()
        # Wrong format
        data.email = "hahahaha.not-valid"
        self.assertRaises(Invalid, IJournalist.validateInvariants, data)

    def test_biography(self):
        self.folder.invokeFactory('Person', 'user1')
        user1 = self.folder['user1']
        adapter = IJournalist(user1)
        adapter.biography = u"somebody, somewhere"
        self.assertEquals(adapter.biography, u"somebody, somewhere" )
