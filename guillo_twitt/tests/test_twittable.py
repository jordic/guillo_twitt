

import pytest

from guillo_twitt.content import Twittable
from guillo_twitt.api import TwittService
from aiohttp import web
import guillotina

from guillo_twitt.api import MaxRetryException

async def return_settings():
    return dict(
        consumer_key="asdf",
        consumer_secret="asdf"
    )


async def test_content_is_urlencoded():
    r = Twittable()
    r.text = "Hola & test"
    assert await r.get_text() == "Hola%20%26%20test"


class ClientThatRetry:
    def __init__(self, ok=1):
        self.tried = 0
        self.failed = None
        self.ok = ok

    async def request(self, method, endpoint, params):
        if self.tried < self.ok:
            self.tried = self.tried + 1
            self.failed = True
            raise web.HTTPBadRequest
        self.tried = self.tried + 1
        return dict(ok="ok")


async def test_twitt_service_should_retry():
    client = ClientThatRetry()
    service = TwittService(dict(), dict())
    result = await service.do_update(client, "test")
    assert result == dict(ok="ok")
    assert client.tried == 2


async def test_should_respect_max_retries():
    client = ClientThatRetry(ok=5)
    service = TwittService(dict(), dict())
    service.get_settings = return_settings
    with pytest.raises(MaxRetryException) as e_info:
        result = await service.do_update(client, "test")


async def test_should_error_if_misconfigured():

    async def failing_credentials():
        return None, None

    service = TwittService(dict(), dict())
    service.get_settings = return_settings
    service.get_oauth_credentials = failing_credentials
    result = await service()
    assert result.status == 412


class OkClient:
    async def request(self, method, endpoint, params):
        class Good:
            async def json(self):
                return dict(ok="ok")
        return Good()


async def test_is_responding(monkeypatch):

    client = OkClient()
    context = Twittable()
    context.text = "hola"
    service = TwittService(context, dict())
    service.get_settings = return_settings

    async def ok_client(token, secret):
        return client

    async def cred():
        return "a", "b"

    service.get_request_client = ok_client
    service.get_oauth_credentials = cred

    result = await service()
    assert result['ok'] == "ok"
