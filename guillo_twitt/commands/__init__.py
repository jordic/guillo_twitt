
import logging
import sys
from guillotina.component import get_utility
from guillotina.interfaces import IApplication

from guillotina.commands import Command
from guillotina.interfaces import IAnnotations
from guillo_twitt.interfaces import ITwittAuthToken
from guillotina import app_settings
from guillotina.registry import REGISTRY_DATA_KEY


from aioauth_client import TwitterClient


logger = logging.getLogger("guillo_twitt")


_root_id = "db"
_container = "container"

NO_KEYS = """TWITTER OAUTH CREDENTIALS MISSING
---
In order to use the addon you must provide twitter API credentials:
TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET
as env variables.
"""


class TwitterAuthorizeApp(Command):
    description = "Generate a token throught PIN-Auth Twitter API"

    async def run(self, arguments, settings, app):
        consumer_key = app_settings['guillo_twitt'].get('consumer_key', '')
        consumer_secret = app_settings['guillo_twitt'].get('consumer_secret', '')  # noqa
        if not consumer_key or not consumer_secret:
            print(NO_KEYS)
            sys.exit(0)
        twitter = TwitterClient(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
        )
        request_token, request_token_secret, _ = await twitter.get_request_token()
        authorize_url = twitter.get_authorize_url(request_token)
        print("Open", authorize_url, "in a browser")
        print("PIN code:")
        oauth_verifier = input()
        # print(f'OAuth Code {oauth_verifier}')
        try:
            oauth_token, oauth_token_secret, _ = await twitter.get_access_token(
                oauth_verifier)
            await self.set_auth_token(oauth_token, oauth_token_secret)
            print(f'OAuth token stored')
        except:
            print("Failed to create tokens for auth")


    async def set_auth_token(self, token, token_secret, container='container'):
        """ This method is ugly, sure it can be cleanup and there is
        a better way of doing this.. I Just want to set some registry keys from
        a command."""
        root = get_utility(IApplication, name='root')
        db = root[_root_id]
        db._db._storage._transaction_strategy = 'none'
        tm = self.request._tm = db.get_transaction_manager()
        self.request._db_id = db.id
        tm = db.get_transaction_manager()
        tm.request = self.request
        self.request._txn = txn = await tm.begin(self.request)
        container = await db.async_get(container)
        acont = IAnnotations(container)
        self.request.container_sesttings = await acont.async_get(
            REGISTRY_DATA_KEY
        )
        registry = self.request.container_sesttings
        reg = registry.for_interface(ITwittAuthToken)
        reg['token'] = token
        reg['token_secret'] = token_secret
        await tm.commit(txn=txn)

