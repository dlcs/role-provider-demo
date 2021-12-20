# Role Provider Demonstrator

Basic app for demonstrating DLCS role-provider functionality.

## Overview

This is a basic app that shows the minimum functionality for a role-provider with no downstream dependency.

## Tech :robot:

* [Flask](https://flask.palletsprojects.com)
* [Flask-Session](https://flask-session.readthedocs.io/en/latest/)
* [Flask-Caching](https://flask-caching.readthedocs.io/en/latest/)
* [Flask-HttpAuth](https://flask-httpauth.readthedocs.io/en/latest/)

## Limitations

Session storage is on disk so sessions can be lost of underlying hardware replaced.

Caching is in-memory, stored sessions will be lost if service restarted.