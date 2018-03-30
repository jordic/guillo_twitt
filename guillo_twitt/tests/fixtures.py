from guillotina.testing import TESTING_SETTINGS
import json
import pytest
import json


TESTING_SETTINGS.update({
    "applications": [
        "guillo_twitt"
    ]
})


from guillotina.tests.conftest import *  # noqa
from guillotina.tests.utils import ContainerRequesterAsyncContextManager  # noqa


class TwittRequester(ContainerRequesterAsyncContextManager):

    async def __aenter__(self):
        requester = await super().__aenter__()
        await requester('POST', '/db/guillotina/@addons', data=json.dumps({
             "id": "guillo_twitt"
        }))
        return requester


@pytest.fixture(scope='function')
async def twitt_requester(guillotina):
    return TwittRequester(guillotina)
