from flask import Flask

app = Flask(__name__)


@app.route("/login")
def login():
    pass


@app.route("/info")
def info():
    pass


@app.route("/roles")
def roles():
    pass
