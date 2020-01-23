from app import app
from app import db
from blog.blueprint import posts

import views

### Blueprint

app.register_blueprint(posts, url_prefix='/')


if __name__=='__main__':
    app.run(port=8000)

