# -*- coding: utf-8 -*-
import logging

import os

from datetime import datetime

from zope.component import queryUtility

from plone.dexterity.interfaces import IDexterityFTI

from Products.CMFCore.utils import getToolByName

from Products.GenericSetup.upgrade import listUpgradeSteps

from s17.person.behaviors.contact import IContactInfo
from s17.person.behaviors.user import IPloneUser


_PROJECT = 'sc.behavior.journalist'
_PROFILE_ID = 'sc.behavior.journalist:default'


def run_upgrades(context):
    ''' Run Upgrade steps
    '''
    if context.readDataFile('sc.behavior.journalist-default.txt') is None:
        return
    logger = logging.getLogger(_PROJECT)
    site = context.getSite()
    setup_tool = getToolByName(site, 'portal_setup')
    version = setup_tool.getLastVersionForProfile(_PROFILE_ID)
    upgradeSteps = listUpgradeSteps(setup_tool, _PROFILE_ID, version)
    sorted(upgradeSteps, key=lambda step: step['sortkey'])

    for step in upgradeSteps:
        oStep = step.get('step')
        if oStep is not None:
            oStep.doStep(setup_tool)
            msg = "Ran upgrade step %s for profile %s" % (oStep.title,
                                                          _PROFILE_ID)
            setup_tool.setLastVersionForProfile(_PROFILE_ID, oStep.dest)
            logger.info(msg)


def demo_steps(context):
    """ Run steps to prepare a demo.
    """
    if context.readDataFile('sc.person.journalist-demo.txt') is None:
        return
    portal = context.getSite()
    portal.invokeFactory('Folder', 'Persons')
    folder = portal['Persons']
    list_users = [{'name':'marcelo-santos', 'password':'marcelo',
                    'number': '1', 'birthday': (1985, 2, 17)},
                 ]


    # Set behaviors to person
    behaviors = ['s17.person.behaviors.user.IPloneUser',
                 'sc.behavior.journalist']
    fti = queryUtility(IDexterityFTI,
                        name='Person')
    fti.behaviors = tuple(behaviors)

    for user in list_users:
        person = user['name']
        fullname = person.split('-')
        birthday = user['birthday']
        #image = None
        #data = getFile(image).read()
        folder.invokeFactory('Person', person,
            birthday=datetime.date(datetime(birthday[0], birthday[1],
                                   birthday[2])),
            #picture=NamedImage(data),
            given_name=fullname[0].capitalize(),
            surname=fullname[1].capitalize(),
            gender=u'm',
            )

        p1_journalist = IJournalist(folder[person])
        p1_journalist.email = u"marcelo.santos@simplesconsultoria.com.br"
        p1_journalist.biography = u"Fictious character, created for testing purposes"
        #p1_ploneuser = IPloneUser(folder[person])
        #p1_ploneuser.user_name = person
        folder[person].reindexObject()
        review_state = folder[person].portal_workflow.getInfoFor(
                                                            folder[person],
                                                            'review_state')
        if not review_state == 'published':
            folder[person].portal_workflow.doActionFor(folder[person],
                                                       'publish')
    review_state = folder.portal_workflow.getInfoFor(folder, 'review_state')
    if not review_state == 'published':
        folder.portal_workflow.doActionFor(folder, 'publish')

    import transaction
    transaction.commit()


