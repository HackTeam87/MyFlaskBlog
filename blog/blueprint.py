import os
from app import *
from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
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


@posts.route('/json')
def json():

    results = [
        {
          "rec_create_date": "12 Jun 2016",
          "rec_dietary_info": "nothing",
          "rec_dob": "01 Apr 1988",
          "rec_first_name": "New",
          "rec_last_name": "Guy",
        },
        {
          "rec_create_date": "1 Apr 2016",
          "rec_dietary_info": "Nut allergy",
          "rec_dob": "01 Feb 1988",
          "rec_first_name": "Old",
          "rec_last_name": "Guy",
        },
    ]

    return jsonify(results)


@posts.route('/')
def allp():
    q = request.args.get('g')

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=5)
   # article = Post.query.order_by(desc(Post.created)).paginate(page, POSTS_PER_PAGE, False).items

    return render_template('posts/all-posts.html', posts=posts, pages=pages )





@posts.route('/blog/one-post=<int:id>',methods = ['GET', 'POST'])
def ps(id):
    articles = Post.query.filter(Post.id == id)

    return render_template('posts/posts.html', articles=articles )




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

            p = Post(title=title,body=body,image=filename)
            db.session.add(p)
            db.session.commit()
        else:
            p = Post(title=title,body=body)
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
            post.image = filename
    else:
        filename = 'Nofile'
    post.title = title
    post.body = body
    db.session.commit()

    return redirect('/')





@posts.route("/blog/delete-post=<int:id>")
def deletep(id):
    p = Post.query.filter(Post.id == id).delete()
    db.session.commit()
    return redirect('/')


