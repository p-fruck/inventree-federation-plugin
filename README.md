# Inventree Federation Plugin

PoC of a federation plugin. This was a first attempt making InvenTree an IdP itself which has been superseeded by [invenhost/inventree-federation](https://github.com/invenhost/inventree-federation).

## Manual setup:

The following section section describes setting up an unidirectional federation between two InvenTree instances.

To get started, clone the InvenTree repository into InvenTree and InvenTree2 (you can choose a more descriptive name yourself).
Get both development setups up and running as described per InvenTree documentation one the following ports:

- InvenTree (8000) will be the OIDC provider
- InvenTree2 (8001) will be the instance we are trying to login with an account provided by InvenTree (Relying Party in OIDC terms).

Both setups likely reqire you execute the following commands, read the official docs for mroe details:

```bash
docker-compose run inventree-dev-server invoke install
docker-compose run inventree-dev-server invoke setup-test
docker-compose run inventree-dev-server invoke update
```

## Configuring InvenTree (OIDC provider)

- Add `django-oidc-provider` to `docker/requirements.txt` (requires a fresh `docker-compose build`)
- Add `oidc_provider` to `INSTALLED_APPS` in `InvenTree/InvenTree/settings.py`
- Add `re_path('accounts/oidc-provider/', include('oidc_provider.urls', namespace='oidc_provider')),` to the `urlpatterns` array in `InvenTree/InvenTree/urls.py`

Run the initial steps required by the django-oidc-provider.

```shell
docker-compose run inventree-dev-server python3 InvenTree/manage.py migrate
docker-compose run inventree-dev-server python3 InvenTree/manage.py creatersakey
```

Next, configure a static IP address for the container. This is not considered a good practice for production, but is useful for development.
To configure a static IP address, add the following config to your compose file:

```yaml
version: '3'
services:
    ...
    inventree-dev-server:
        ...
        environment:
            INVENTREE_ALLOWED_HOSTS: 127.0.0.1,localhost,172.16.238.10
            ...
        networks:
            default: {}
            inventree-static:
                ipv4_address: 172.16.238.10
...
networks:
    inventree-static:
    ipam:
        driver: default
        config:
        - subnet: "172.16.238.0/24"
```

Start the service and login to the admin UI. In the OIDC Provider section, create a new Client and set `http://172.16.238.11:8000/accounts/<PROVIDER_ID>/login/callback/` as the redirect URI (note the trailing slash). `PROVIDER_ID` can be set to `inventree`. Django will create an OIDC `client_id` and `secret` for you.

## Configuring InvenTree2 (Relying Party)

Make sure you are using the latest development version of InvenTree since my upstreamed changes have not yet been included in a stable release.

In the `docker-compose.yml` add the following config to the `inventree-dev-server`:

```yaml
    inventree-dev-server:
        container_name: inventree-dev-server
        ...
        environment:
            INVENTREE_SOCIAL_BACKENDS: allauth.socialaccount.providers.openid_connect
            INVENTREE_SOCIAL_PROVIDERS: |
                "openid_connect": {
                    "id": "<PROVIDER_ID>",
                    "name": "InvenTree",
                    "server_url": "http://<INVENTREE_HOST>:8000/accounts/oidc-provider/.well-known/openid-configuration",
                    "APP": {
                        "client_id": "<OIDC_CLIENT_ID>",
                        "secret": "<OIDC_SECRET>"
                    }
                }
            INVENTREE_ALLOWED_HOSTS: 127.0.0.1,localhost,172.16.238.11
            ...
        networks:
            default: {}
            inventree_inventree-static:
                ipv4_address: 172.16.238.11
    ...
networks:
   inventree_inventree-static:
    driver: bridge
    external: true
```

Notes:

- Replace `INVENTREE_HOST`, `OIDC_CLIENT_ID` and `OIDC_SECRET` with your actual values. Make sure to use the same `PROVIDER_ID` as for the InvenTree OIDC Client redirect URI.
- The external network is called `inventree_inventree-static` because the `COMPOSE_PROJECT_NAME` of the OIDC Provider (default to the name of the directory the compose file is located in) is `inventree`. Might need to be adapted for your local setup.
- The external network must already exist, the OIDC Provider must therefore be started before the relying party
- The IP addresses can only be accessed by the host system if docker/podman is run in rootfull mode

To enable sign-in using SSO, activate `Enable SSO` under `Settings > Login Settings > Single Sign On`. Also, the `INVENTREE_EMAIL_HOST` variable must be specified. A working email server is not required, setting the value to `localhost` is also fine, see [this issue](https://github.com/inventree/InvenTree/issues/4553) for more details.
