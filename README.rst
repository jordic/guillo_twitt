guillo_twitt Docs
==================================

This is a demo/experiment with guillotina to add an extension to allow
contenttype inherited/based on twittable to be twittable.

For the prupose of the demo, there is the Twitter OAuth PIN auth implemented,
anyway on a serious CMS this has to be done with an UI and the diferent oauth
steps.

To run de demo, you must install the addon, and boot the server

For booting guillotina with the addon, you must provide,
credentials for your twitter app created, as env variables:

TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET

Later, you need to authenticate  the app and get the secret tokens
using the command:

g twitt_auth

After that you are ready to start twitting items, just pust a Twittable
content, and you will have a "tool" /db/content/twittable-item/@twitt
where you can POST to twit.



Dependencies
------------

Python >= 3.6


Installation
------------

This example will use virtualenv::

  virtualenv .
  ./bin/python setup.py develop


Running
-------

Most simple way to get running::

  ./bin/guillotina


Running Postgresql Server:

    docker run --rm -e POSTGRES_DB=guillotina -e POSTGRES_USER=guillotina -p 127.0.0.1:5432:5432 --name postgres postgres:9.6
