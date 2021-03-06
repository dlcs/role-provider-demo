import json
import os
import uuid
from flask import Flask, render_template, session, request, redirect, abort, jsonify
from flask_session import Session
from flask_caching import Cache
from flask_httpauth import HTTPBasicAuth

SESSION_KEY = "session_user"
ACCESS_KEY = os.environ.get("ACCESS_KEY")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")
DLCS_ROOT = os.environ.get("DLCS_ROOT", "dlcs.digirati.io")
DLCS_CUSTOMER = int(os.environ.get("DLCS_CUSTOMER", 2))
DLCS_AUTHSERVICE = os.environ.get("DLCS_AUTHSERVICE")

auth = HTTPBasicAuth()

app = Flask("dlcs-role-provider")

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 600,
    "CACHE_THRESHOLD": 100,
    "SESSION_TYPE": "filesystem",
    "SESSION_PERMANENT": False,
    "SESSION_USE_SIGNER": True,
    "SESSION_KEY_PREFIX": "dlcs_rp:",
    "SESSION_FILE_THRESHOLD": 100,
}
app.config.from_mapping(config)

# flask_session
app.secret_key = os.environ.get("FLASK_SECRET")
Session(app)

# flask_cache
cache = Cache(app)

settings = {}


@app.before_first_request
def startup():
    with open("settings.json") as settings_json:
        global settings
        settings = json.load(settings_json)


@app.route("/login", methods=["GET"])
def login():
    """
    Handle GET requests for login page.
    Renders login page if user unknown or redirects back to DLCS if user is known
    """

    # if user has an active session, redirect to dlcs
    if session_user := session.get(SESSION_KEY, {}):
        return _redirect_to_dlcs(session_user)

    # else render login page
    return _render_login()


@app.route("/login", methods=["POST"])
def do_login():
    """
    Handle POST requests for login page.
    This renders the login page for user to authenticate.
    Once authenticated, user is logged in and a session is established containing accessible roles.
    """

    username = request.form["username"]
    password = request.form["password"]
    dlcs_root = request.form["dlcs"] or DLCS_ROOT
    dlcs_customer = request.form["customer"] or DLCS_CUSTOMER

    success, user_roles = _verify_auth(username, password)

    if success:
        # create session
        session_key = str(uuid.uuid4())
        session_user = {
            "token": session_key,
            "dlcs_root": dlcs_root,
            "roles": user_roles,
            "customer": dlcs_customer
        }
        session[SESSION_KEY] = session_user

        # cache user-roles for later retrieval
        cache.set(_get_roles_cache_key(session_key), user_roles)

        # redirect to DLCS with a session id
        return _redirect_to_dlcs(session_user)
    else:
        # re-render template with an error
        return _render_login(error="Unknown Credentials")


@app.route("/roles", methods=["POST"])
@auth.login_required
def roles():
    """
    Return list of roles for token specified in ?token= query parameter
    """

    args = request.form
    if token := args.get("token", None):
        if cached_roles := cache.get(_get_roles_cache_key(token)):
            return jsonify(cached_roles)

    abort(404, description="Resource not found")


@app.route("/logout", methods=["GET"])
def logout():
    """
    Remove user session.
    This can be helpful if session exists but cached roles do not.
    """
    if session_user := session.get(SESSION_KEY, {}):
        cache.delete(_get_roles_cache_key(session_user["token"]))

    session[SESSION_KEY] = {}
    return _render_login(message="User logged out")


@auth.verify_password
def verify_user(username, password):
    return username == ACCESS_KEY and password == ACCESS_SECRET


def _render_login(error=None, message=None):
    return render_template("login.html",
                           default_customer=DLCS_CUSTOMER,
                           default_root=DLCS_ROOT,
                           users=settings["users"],
                           error=error,
                           message=message)


def _verify_auth(username: str, password: str):
    for user in settings["users"]:
        if user["username"] == username and user["password"] == password:
            return True, user["roles"]

    return False, []


def _redirect_to_dlcs(session_user: dict):
    dlcs_root = session_user["dlcs_root"]
    dlcs_customer = session_user["customer"]
    session_key = session_user["token"]
    return redirect(f"https://{dlcs_root}/auth/{dlcs_customer}/{DLCS_AUTHSERVICE}?token={session_key}")


def _get_roles_cache_key(token: str):
    return f"roles_{token}"


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
