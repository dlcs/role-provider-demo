# Role Provider Demonstrator

Basic app for demonstrating DLCS role-provider functionality.

## Overview

This is a basic app that shows the minimum functionality for a role-provider with no downstream dependency.

## Getting Started

The app can be built and run via the included dockerfile, for example:

```bash
docker build -t role-provider:local .

docker run --name dlcs-role-provider -it --rm -p 8083:80 --env-file .env role-provider:local
```

alternatively, it can be run via the included docker-file:

```bash
docker-compose up
```

## Configuration

### Environment Variables

The app requires 3 environment variables to run, see `.env.dist` for samples:

* `FLASK_SECRET` - Flask [`secret_key`](https://flask.palletsprojects.com/en/2.0.x/config/#SECRET_KEY) value
* `ACCESS_KEY` - Basic auth username for access roles for token.
* `ACCESS_SECRET` - Basic auth password for access roles for token.
* `DLCS_ROOT` - The default DLCS root to use for testing (without `https://`). Can be specified at login.
* `DLCS_CUSTOMER` - The DLCS customer to use for testing. Can be specified at login.

### `settings.json`

`settings.json` contains an array of known user credentials and their roles, each "user" contains:

* `username` - user login name
* `password` - user password
* `roles` - an array of roles this user has

e.g.

```json
[{
    "username": "superuser",
    "password": "superuser",
    "roles": [
        "http://dlcs-role-provider/roles/clickthrough",
        "http://dlcs-role-provider/roles/restricted",
        "http://dlcs-role-provider/roles/secret"
    ]
}]

```

## Tech :robot:

* [Flask](https://flask.palletsprojects.com)
* [Flask-Session](https://flask-session.readthedocs.io/en/latest/)
* [Flask-Caching](https://flask-caching.readthedocs.io/en/latest/)
* [Flask-HttpAuth](https://flask-httpauth.readthedocs.io/en/latest/)

## Limitations

Session storage is on disk so sessions can be lost of underlying hardware replaced.

Caching is in-memory, stored sessions will be lost if service restarted.