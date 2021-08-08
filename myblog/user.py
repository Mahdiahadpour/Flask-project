from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename


bp = Blueprint("user", __name__,url_prefix='/user')


@bp.route("/profile/")
def profile():
    return render_template('')



@bp.route("/posts-list/")
def post_list():
    return render_template('')



@bp.route("/create-post/")
def create_post():
    return render_template('')


@bp.route("/edit-post/<post_id>")
def edit_post(post_id):
    return render_template('')

