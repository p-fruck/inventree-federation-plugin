# Inventree Federation Plugin

PoC of a federation plugin for InvenTree

## Manual workarounds:

- Add `django-oidc-provider` to `docker/requirements.txt` (requires `docker-compose build`)
- Add `oidc_provider` to `INSTALLED_APPS` in `InvenTree/settings.py`

```shell
docker-compose run inventree-dev-server python3 InvenTree/manage.py migrate
docker-compose run inventree-dev-server python3 InvenTree/manage.py creatersakey
```