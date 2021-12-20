from flask import Flask, render_template

app = Flask("dlcs-role-provider")


@app.route("/login", methods=['GET'])
def login():
    return render_template("login.html")


@app.route("/info")
def info():
    pass


@app.route("/roles")
def roles():
    pass


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
