# Role Provider Demonstrator

Basic app for demonstrating DLCS role-provider functionality.

## Overview

This is a basic app that shows the minimum functionality for a role-provider with no downstream dependency.

## Configuration

### Environment Variables

The app requires 3 environment variables to run, see `.env.dist` for samples:

* `FLASK_SECRET` - Flask [`secret_key`](https://flask.palletsprojects.com/en/2.0.x/config/#SECRET_KEY) value
* `ACCESS_KEY` - Basic auth username for access roles for token.
* `ACCESS_SECRET` -Basic auth password for access roles for token. 

### `settings.json`

`settings.json` contains non-secret configuration:

* `"dlcs-default-root"` - the default DLCS root to use for testing (without `https://`). Can be specified at login.
* `"dlcs-customer"` - the DLCS customer to use for testing. Can be specified at login.
* `"users"` - an array of objects specifying valid login credentials and roles.

## Tech :robot:

* [Flask](https://flask.palletsprojects.com)
* [Flask-Session](https://flask-session.readthedocs.io/en/latest/)
* [Flask-Caching](https://flask-caching.readthedocs.io/en/latest/)
* [Flask-HttpAuth](https://flask-httpauth.readthedocs.io/en/latest/)

## Limitations

Session storage is on disk so sessions can be lost of underlying hardware replaced.

Caching is in-memory, stored sessions will be lost if service restarted.