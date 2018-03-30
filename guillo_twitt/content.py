
from zope.interface import Interface
from guillotina import schema
from guillotina import content
from guillotina import configure

from guillo_twitt.interfaces import ITwittable

import urllib.parse

@configure.contenttype(
    type_name='Twittable',
    schema=ITwittable,
    behaviors=[
        'guillotina.behaviors.dublincore.IDublinCore',
    ]
)
class Twittable(content.Item):

    async def get_text(self):
        return urllib.parse.quote(self.text)
