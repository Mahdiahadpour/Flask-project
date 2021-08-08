import functools
from flask import Blueprint, session
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from myblog.db import get_db


bp = Blueprint("blog", __name__)


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().user.find_one({"_id":ObjectId(user_id)})



def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view




@bp.route("/home")
@bp.route("/")
def home():
    return render_template('index.html')



@bp.route("/post/<post_id>/")
def post(post_id):
    db = get_db()
    post = db.posts.find({'_id':ObjectId(post_id)})
    return render_template('post.html',post=post)



@bp.route("/category-posts/<category_id>/")
def category(category_id):
    return render_template('')


@bp.route("/tag-posts/<tag_id>")
def tag(tag_id):
    return render_template('')



@bp.route("/register", methods=("GET", "POST"))
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get('email')
        phone = request.form.get('phone')
        image = request.files.get('image')
        if image != '':
            image.save('myblog/static/media/uploads/'+secure_filename(image.filename))
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif db.user.find_one({"username":username}) is not None :
            error = f"User {username} is already registered."

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            user = {'username':username,'password':generate_password_hash(password),
                    'email':email,'phone':phone,'image':image.filename}
            db.user.insert_one(user)
            return redirect(url_for("blog.login"))
        else:
            flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        error = None

        user = db.user.find_one({"username":username})

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            user['_id'] = str(user['_id'])
            session["user_id"] = user["_id"]
            return redirect(url_for("blog.home"))
        else:
            flash(error)

    return render_template("auth/login.html")

