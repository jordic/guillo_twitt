

from guillotina import schema
from guillotina.i18n import MessageFactory
from zope.interface import Interface

_ = MessageFactory("guillo_twitt")


class ITwittAuthToken(Interface):
    token = schema.TextLine(title=_('Token'))
    token_secret = schema.TextLine(title=_('Token Secret'))


class ITwittable(Interface):
    text = schema.Text()