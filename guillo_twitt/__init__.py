from guillotina import configure
import os

app_settings = {
    # provide custom application settings here...
    'guillo_twitt': {},
    "commands": {
        "twitt_auth": "guillo_twitt.commands.TwitterAuthorizeApp"
    }
}

# TODO: load secrets from secrets k8 api
# usually read them from a mounted volume on pod.
from_env = dict(
    consumer_key=os.getenv(
        "TWITTER_CONSUMER_KEY", None
    ),
    consumer_secret=os.getenv(
        "TWITTER_CONSUMER_SECRET",
        None
    )
)
app_settings['guillo_twitt'].update(from_env)


# TODO: Define specific permissions for users allowed to twitt content

def includeme(root):
    """
    custom application initialization here
    """
    configure.scan('guillo_twitt.content')
    configure.scan('guillo_twitt.api')
    configure.scan('guillo_twitt.install')

