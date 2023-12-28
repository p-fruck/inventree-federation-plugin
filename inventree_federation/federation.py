import logging

from django.conf.urls import url
from django.urls import include
from plugin import InvenTreePlugin
from plugin.mixins import AppMixin, UrlsMixin

# from oidc_provider.models import Client, ResponseType


logger = logging.getLogger('inventree')


class FederationPlugin(AppMixin, UrlsMixin, InvenTreePlugin):
    SLUG = "federation"
    NAME = "FederationPlugin"
    TITLE = "Federation Plugin"

    # register oidc provider
    URLS = [
        # url(r'^openid/', include('oidc_provider.urls', namespace='oidc_provider')),
    ]

    def __init__(self):
        super().__init__()

        logger.info("Starting Federation Plugin")

        # dummy_client = Client.objects.filter(client_id="dummy")
        # if dummy_client:
            # print("Dummy Client: dummy_client")
        # else:
            # c = Client(name='Dummy Client', client_id='dummy', client_secret='secret', redirect_uris=['http://example.com/'])
            # c.save()
            # c.response_types.add(ResponseType.objects.get(value='code'))
