import json
import os
import uuid
from flask import Flask, render_template, session, request, redirect
from flask_session import Session

app = Flask('dlcs-role-provider')

app.secret_key = os.environ.get('FLASK_SECRET')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'dlcs_rp:'
app.config['SESSION_FILE_THRESHOLD'] = 100
Session(app)

settings = {}


@app.before_first_request
def startup():
    with open('settings.json') as settings_json:
        global settings
        settings = json.load(settings_json)


@app.route("/login", methods=['GET'])
def login():
    # do we know this user? If so redirect
    return _render_login()


@app.route("/login", methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    dlcs_root = request.form['dlcs'] or settings['dlcs-default-root']
    dlcs_customer = request.form['customer'] or settings['dlcs-customer']

    success, user_roles = _verify_auth(username, password)

    if success:
        # create session
        session_key = str(uuid.uuid4())
        session[session_key] = {
            "dlcs_root": dlcs_root,
            "roles_acquired": 1,
            "roles": user_roles,
            "customer": dlcs_customer
        }

        # redirect to DLCS with a session id
        return redirect(f"https://{dlcs_root}/auth/{dlcs_customer}/fromcas?token={session_key}")
    else:
        # re-render template with an error
        return _render_login('Unknown Credentials')


@app.route("/info")
def info():
    # render roles template
    pass


@app.route("/roles")
def roles():
    # return JSON object, check basic auth credentials
    pass


def _render_login(error=None):
    return render_template('login.html',
                           default_customer=settings['dlcs-customer'],
                           default_root=settings['dlcs-default-root'],
                           users=settings['users'],
                           error=error)


def _verify_auth(username: str, password: str):
    for user in settings['users']:
        if user['username'] == username and user['password'] == password:
            return True, user['roles']

    return False, []


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
