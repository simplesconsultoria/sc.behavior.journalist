# coding: utf-8

from plone.directives import form
from Products.CMFDefault.utils import checkEmailAddress
from s17.person.content.person import IPerson
from sc.behavior.journalist import MessageFactory as _
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.interface import implements, alsoProvides


class IJournalist(form.Schema):
    """Add fields to Person
    """
    email = schema.TextLine(
        title=_(u"Email"),
        description=_(u"Email address of the journalist."),
        required=False,
    )

    resume = schema.Text(
        title=_(u"Résumé"),
        description=_(u"A short biografy of the journalist."),
        required=False
    )

    signature = schema.TextLine(
        title=_(u"Signature"),
        description=_(
            u"Stylized version of journalist's name to be used in bylines."
        ),
        required=False,
    )

alsoProvides(IJournalist, form.IFormFieldProvider)


@form.validator(field=IJournalist['email'])
def validateEmailAddress(value):
    """Validate an email, if provided.
    """
    if not value:
        return True

    checkEmailAddress(value)


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
        return self.annotation.get('s17.person.journalist_email', u"")

    @email.setter
    def email(self, value):
        self.annotation['s17.person.journalist_email'] = value

    @property
    def resume(self):
        return self.annotation.get('s17.person.resume', u"")

    @resume.setter
    def resume(self, value):
        self.annotation['s17.person.resume'] = value

    @property
    def signature(self):
        return self.annotation.get('s17.person.signature', u"")

    @signature.setter
    def signature(self, value):
        self.annotation['s17.person.signature'] = value
