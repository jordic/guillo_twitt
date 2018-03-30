
from guillotina import configure
from guillotina.addons import Addon
from guillo_twitt.interfaces import ITwittAuthToken


@configure.addon(
    name="guillo_twitt",
    title="A Service for twitting content items")
class ManageAddon(Addon):

    @classmethod
    def install(cls, container, request):
        registry = request.container_settings  # noqa
        registry.register_interface(ITwittAuthToken)
        tauth = registry.for_interface(ITwittAuthToken)
        tauth['token'] = None
        tauth['token_secret'] = None
        # install logic here...

    @classmethod
    def uninstall(cls, container, request):
        registry = request.container_settings  # noqa
        # uninstall logic here...
