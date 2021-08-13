from bson import ObjectId
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
import json
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from myblog.blog import login_required
from myblog.db import get_db

bp = Blueprint("user", __name__,url_prefix='/user')

@login_required
@bp.route("/profile/")
def profile():
    return render_template('')



@bp.route("/posts-list/")
def post_list():
    user = g.user
    posts = get_db().posts.find({'user':user})
    return render_template('all_posts.html',posts=posts)



@bp.route("/create-post/",methods=['GET','POST'])
def create_post():
    if request.method == 'POST':

        db = get_db()
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        tag = json.loads(request.form.get('tags'))
        image = request.files.get('image')
        user = g.user
        status = True

        if image != '':
            image.save('myblog/static/media/uploads/posts/'+secure_filename(image.filename))

        post = db.user.find_one({"title":title})
        if post is None:
            db.posts.insert_one({'user':user,'title':title,'content':content,
                                'category':category,
                             'tag':tag,'image':image.filename,
                             'status':status,'like':[],'dislike':[]})


            return redirect(url_for('blog.home'))
        else:
            flash('This post has already exists!')



    return render_template('new_post.html')


@bp.route("/edit-post/<post_id>")
def edit_post(post_id):
    return render_template('')

