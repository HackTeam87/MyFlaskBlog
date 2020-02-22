import os
from app import *
from flask import Blueprint, render_template, request, url_for, send_from_directory, redirect, flash, jsonify
from models import  Post
from sqlalchemy import asc, desc
from flask_security import login_required
from random import sample
###  Upload_files
#from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
POSTS_PER_PAGE = 1


posts = Blueprint('posts', __name__, static_folder='fstatic', template_folder='templates')

ALLOWED_EXTENSIONS = set(['ico','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@posts.route('/imageuploader', methods=['GET','POST'])
def imageuploader():
    file = request.files.get('file')
    if file:
        filename = file.filename.lower()
        fn, ext = filename.split('.')
        if ext in ['jpg', 'pdf', 'gif', 'png', 'jpeg']:
            img_fullpath = os.path.join(app.config['BLOG_UPLOAD_FOLDER'], filename)
           # img_fullpath = app.config['BLOG_UPLOAD_FOLDER'] + filename
            print(img_fullpath)
            file.save(img_fullpath)
            return jsonify({'location' : filename})

    # fail, image did not upload
    output = make_response(404)
    output.headers['Error'] = 'Image failed to upload'
    return output


@posts.route('/<path:filename>')
@posts.route('/blog/<path:filename>')
def custom_static(filename):
    return send_from_directory('/home/grin/generator/blog/static/files', filename)
    #return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)


@posts.route('/chart')
def charts():

     return render_template('posts/chart.html')


@posts.route('/editor')
def editor():

     return render_template('posts/editor.html')



@posts.route('/data')
def data():

    return jsonify({'results' : sample(range(1,20),15)})





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

    pages = posts.paginate(page=page, per_page=8)
   # article = Post.query.order_by(desc(Post.created)).paginate(page, POSTS_PER_PAGE, False).items

    return render_template('posts/all-posts.html', posts=posts, pages=pages )


#Domofon
@posts.route('blog/phone')
def phone():

    domofon = Post.query.filter(Post.id == '159')
    return render_template('posts/domofon.html', title='Domofon', domofon=domofon)



@posts.route('blog/one-post=<int:id>',methods = ['GET', 'POST'])
@login_required
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
@login_required
def deletep(id):
    p = Post.query.filter(Post.id == id).delete()
    db.session.commit()
    return redirect('/')


