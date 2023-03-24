# Inventree Federation Plugin

PoC of a federation plugin for InvenTree (still in some pre-alpha state)

## Manual setup:

The following section section describes setting up an unidirectional federation between two InvenTree instances.

To get started, clone the InvenTree repository into InvenTree and InvenTree2 (you can choose a more descriptive name yourself).
Get both development setups up and running as described per InvenTree documentation one the following ports:

- InvenTree (8000) will be the OIDC provider
- InvenTree2 (8001) will be the instance we are trying to login with an account provided by InvenTree (Relying Party in OIDC terms).

## Configuring InvenTree (OIDC provider)

- Add `django-oidc-provider` to `docker/requirements.txt` (requires a fresh `docker-compose build`)
- Add `oidc_provider` to `INSTALLED_APPS` in `InvenTree/InvenTree/settings.py`
- Add `re_path('accounts/oidc-provider/', include('oidc_provider.urls', namespace='oidc_provider')),` to the `urlpatterns` array in `InvenTree/InvenTree/urls.py`

Run the initial steps required by the django-oidc-provider.

```shell
docker-compose run inventree-dev-server python3 InvenTree/manage.py migrate
docker-compose run inventree-dev-server python3 InvenTree/manage.py creatersakey
```

Start the service and login to the admin UI. In the OIDC Provider section, create a new Client and set `http://<INVENTREE2_HOST>:8001/accounts/<PROVIDER_ID>/login/callback/` as the redirect URI (note the trailing slash). `PROVIDER_ID` can be set to `inventree`. Django will create an OIDC `client_id` and `secret` for you.

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
```

Replace `INVENTREE_HOST`, `OIDC_CLIENT_ID` and `OIDC_SECRET` with your actual values. Make sure to use the same `PROVIDER_ID` as for the InvenTree OIDC Client redirect URI
