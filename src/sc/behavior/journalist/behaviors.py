# coding: utf-8

"""Behavior to allow one single e-mail address
and a short biography to sc.person.Person
"""

from zope.annotation.interfaces import IAnnotations

from zope.interface import implements, alsoProvides
from zope.component import adapts

from plone.directives import form
from zope import schema

from s17.person.content.person import IPerson

from sc.behavior.journalist import MessageFactory as _

class IJournalist(form.Schema):
    """Add fields to Person
    """

    email = schema.TextLine(
            title=_(u"e-mail"),
            description=_(u"Single e-mail"),
            required=False,
        )

    resume = schema.Text(
                title=_(u"Résumé"),
                description=_(u"Short biography describing the person -"
                u" suitable to be displayed in a portlet along posts"),
                required=False
            )

alsoProvides(IJournalist, form.IFormFieldProvider)

class Journalist(object):
    """Stores the extra fields in the anotation
    """
    implements(IJournalist)
    adapts(IPerson)

    def __init__(self, context):
        self.context = context
        self.annotation = IAnnotations(self.context)

    @property
    def email(self):
        return self.annotation.get('s17.person.journalist_email', [])

    @email.setter
    def email(self, value):
        self.annotation['s17.person.journalist_email'] = value

    @property
    def resume(self):
        return self.annotation.get('s17.person.resume', [])

    @resume.setter
    def resume(self, value):
        self.annotation['s17.person.resume'] = value
