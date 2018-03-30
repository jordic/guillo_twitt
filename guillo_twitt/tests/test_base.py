
from guillo_twitt.commands import TwitterAuthorizeApp


reg_key = 'guillo_twitt.interfaces.ITwittAuthToken.token'
reg_key_secret = 'guillo_twitt.interfaces.ITwittAuthToken.token_secret'

async def test_ensure_addon_is_installed(twitt_requester):
    async with twitt_requester as requester:
        resp, status_code = await requester('GET', '/db/guillotina/')
        assert status_code == 200
        resp, status_code = await requester('GET', '/db/guillotina/@addons')
        assert "guillo_twitt" in resp['installed']


async def test_registry_token_prop_is_set(twitt_requester):
    async with twitt_requester as r:
        resp, status = await r('GET', '/db/guillotina/@registry')
        assert len(resp['value']) == 4
        assert reg_key in resp['value'].keys()
        assert status == 200
        resp, status = await r('GET', f'/db/guillotina/@registry/{reg_key}')
        assert status == 200


async def test_token_is_set(twitt_requester):
    async with twitt_requester as r:
        app = TwitterAuthorizeApp()
        await app.set_auth_token("xxx", "xxx.1", container='guillotina')
        resp, status = await r('GET', f'/db/guillotina/@registry/{reg_key}')
        assert resp['value'] == 'xxx'
        resp, status = await r('GET', f'/db/guillotina/@registry/{reg_key_secret}')
        assert resp['value'] == 'xxx.1'
