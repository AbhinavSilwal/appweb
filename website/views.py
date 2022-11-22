from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Post, User, Comment
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def createpost():
    if request.method == "POST":
        topic = request.form.get('Topic')
        message = request.form.get('message')

        if not topic and message:
            flash("Fill up the information!", category='error')

        else:
            post = Post(topic=topic, author=current_user.id, message=message)
            db.session.add(post)
            db.session.commit()
            flash("Your Post has been created!", category='error')
            return redirect(url_for('views.allforums'))
    return render_template('createpost.html')

@views.route('/forums-all', methods=['GET', 'POST'])
@login_required
def allforums():
    posts = Post.query.all()

    return render_template('allpost.html', user=current_user, posts=posts)


@views.route('/forums', methods=['GET', 'POST'])
@login_required
def forums():
    
    return render_template('forums.html')


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.forums'))


#    Using this after i get my template

# @views.route("/user/<username>")
# @login_required
# def userprofile(username):
#     return render_template('profile.html')

# @views.route("/profile")
# @login_required
# def profile(username):
#     return render_template('profile.html')
# 
# 
# @views.route("/user/post/<email>")
# @login_required
# def profile(email):
#     posts = Post.query.filter_by(email=email).all()

#     return render_template('userpost.html', user=current_user, posts=posts)

@views.route("/user/posts/<email>")
@login_required
def posts(email):
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("userpost.html", user=current_user, posts=posts, email=email)


@views.route("/post/<id>", methods=['GET', 'POST'])
@login_required
def editpost(id):
    posts = Comment.query.filter_by(id=id)
    if request.method == "POST":
        message = request.form.get('message')

        if not message:
            return redirect(url_for('views.editpost'))

        else:
            message = Comment(author=current_user.id, message=message)
            db.session.add(message)
            db.session.commit()
            flash("Your Post has been created!", category='error')
            return render_template("fpost.html", user=current_user, posts=posts, id=id)

        



    return render_template("post.html", user=current_user, posts=posts, id=id)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.allforums'))