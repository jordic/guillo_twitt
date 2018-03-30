from guillotina import configure
from guillotina import app_settings
from guillotina.browser import ErrorResponse
from guillotina.api.service import Service
from guillotina.i18n import default_message_factory as _
from aiohttp import web

from guillo_twitt.interfaces import ITwittable
from guillo_twitt.interfaces import ITwittAuthToken
from aioauth_client import TwitterClient


import logging

logger = logging.getLogger("twitt")


class MaxRetryException(Exception):
    pass


@configure.service(
    method='POST', name='@twitt',
    permission='guillotina.AccessContent',
    context=ITwittable)
class TwittService(Service):

    MAX_TRIED = 2

    def __init__(self, context, request):
        self.tried = 0
        super(TwittService, self).__init__(context, request)

    async def get_oauth_credentials(self):
        csettings = self.request.container_settings
        registry = csettings.for_interface(ITwittAuthToken)
        return registry['token'], registry['token_secret']

    async def get_request_client(self, token, token_secret):
        settings = app_settings['guillo_twitt']
        return TwitterClient(
            consumer_key=settings['consumer_key'],
            consumer_secret=settings['consumer_secret'],
            oauth_token=token,
            oauth_token_secret=token_secret
        )

    async def do_update(self, client, text):
        try:
            resp = await client.request(
                'POST', 'statuses/update.json', dict(status=text)
            )
            return resp
        except web.HTTPBadRequest:
            self.tried = self.tried + 1
            if self.tried < self.MAX_TRIED:
                resp = await self.do_update(client, text)
                return resp
            else:
                raise MaxRetryException()

    async def get_settings(self):
        return app_settings["guillo_twitt"]

    async def __call__(self):
        settings = await self.get_settings()
        if not settings['consumer_key'] or not settings['consumer_secret']:
            return ErrorResponse(
                'Missconfigured',
                _("Consumer Kye or Consumer secret missing"),
                status=412
            )
        token, token_secret = await self.get_oauth_credentials()
        if not token or not token_secret:
            return ErrorResponse(
                'Missconfigured',
                _("Twitter Oauth credentials not provided"),
                status=412
            )
        logger.debug(f'twitter request')
        client = await self.get_request_client(token, token_secret)
        text = await self.context.get_text()
        resp = await self.do_update(client, text)
        return await resp.json()



