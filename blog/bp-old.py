import os
from app import *
from flask import Blueprint, render_template, request, url_for, redirect, flash
from models import  Post
from sqlalchemy import asc, desc
###  Upload_files
from werkzeug.utils import secure_filename
POSTS_PER_PAGE = 1


posts = Blueprint('posts', __name__, static_folder='fstatic', template_folder='templates')

ALLOWED_EXTENSIONS = set(['ico','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@posts.route('/',methods = ['GET', 'POST'])
@posts.route('/blog/<int:page>',methods = ['GET', 'POST'])
def ps(page = 1):
    article = Post.query.order_by(desc(Post.created)).paginate(page, POSTS_PER_PAGE, False).items
    return render_template('posts/posts.html',article=article)




@posts.route('/new-post')
def newp():
    return render_template('posts/new-post.html')



@posts.route("/post-add",methods = ['POST', 'GET'])
def padd():
    title = request.form.get('title')
    body = request.form.get('body')
    image = request.form.get('image')

    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = 'NoFile' 
    p = Post(title=title, body=body, image=filename)
    db.session.add(p)
    db.session.commit()



    return redirect('/')


@posts.route("/blog/edit-post=<int:id>")
def editp(id):
    post = Post.query.filter(Post.id == id)
    return render_template('posts/edit-post.html',post=post)







@posts.route("/blog/post-edit=<int:id>", methods=['GET', 'POST'])
def pedit(id):
    post = Post.query.filter(Post.id == id).first()

    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        image = request.form.get('image')
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        post.title = title
        post.body = body
        post.image = filename
        db.session.commit()
    else:
        filename = 'NoFile'

    return redirect('/')





@posts.route("/blog/delete-post=<int:id>")
def deletep(id):
    p = Post.query.filter(Post.id == id).delete()
    db.session.commit()
    return redirect('/')


