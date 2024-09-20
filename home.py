import os, sqlite3

from flask import Flask, render_template, url_for, g, request, abort
from FDataBase import FDataBase


DATABASE = "/learning_py.db"
DEBUG = True
SECRET_KEY = ""

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "learning_py.db")))

def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

#
def create_db():
    db = connect_db()
    with app.open_resource("sq_db.sql", mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close() 
#

def get_db():
    if not hasattr(g, 'link_db'):

        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def data_db():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

@app.route("/")
def index():
    print(url_for("index"))
    return render_template("index.html", title="Home page", menu=dbase.getMenu(), posts=dbase.getPostsAnonce())

@app.route("/learn")
def learn():
    return "<h1>Learn right here</h1>"


@app.route("/install", methods=["POST", "GET"])
def install():
    if request.method == "POST":
        res = dbase.addPost(request.form["name"], request.form["post"], request.form["url"])

    return render_template("install.html", title="Add new Post!", menu=dbase.getMenu())

@app.route("/post/<alias>")
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)
    
    return render_template("post.html", menu=dbase.getMenu(), title=title, post=post)

@app.route("/more")
def more():
    return "<h1>More right here</h1>"

@app.route("/profile/<username>")
def profile(username):
    return f"Good afternoon {username}!"

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.errorhandler(404)
def pageNotFound(error):
    return render_template("error404.html", title="Oops, Error"), 404   

if __name__ == "__main__":
    app.run(debug=True)

