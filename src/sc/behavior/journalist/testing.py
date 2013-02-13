# -*- coding: utf-8 -*-

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.testing.z2 import ZSERVER_FIXTURE


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import sc.behavior.journalist
        self.loadZCML(package=sc.behavior.journalist)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'sc.behavior.journalist:default')


class FixtureDemo(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        portal.portal_workflow.setChainForPortalTypes(
            ['Folder', 'Person'],
            ['simple_publication_workflow'])
        self.applyProfile(portal, 'sc.behavior.journalist:demo')


FIXTURE = Fixture()
DEMO_FIXTURE = FixtureDemo()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='sc.behavior.journalist:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, DEMO_FIXTURE, ZSERVER_FIXTURE,),
    name='sc.behavior.journalist:Functional',
)
