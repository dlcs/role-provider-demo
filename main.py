import json
from flask import Flask, render_template

app = Flask("dlcs-role-provider")

settings = {}


@app.before_first_request
def startup():
    with open('settings.json') as settings_json:
        global settings
        settings = json.load(settings_json)


@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html', default_root=settings['dlcs-default-root'], users=settings['users'])


@app.route("/info")
def info():
    pass


@app.route("/roles")
def roles():
    pass


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
