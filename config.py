class Configuration(object):
    DEBUG = True
    UPLOAD_FOLDER = '/home/grin/generator/static/img/blogimgage'
#    MYSQL_DATABASE_CHARSET = 'utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://grin:golden1306!@localhost/blog?charset=utf8'
    SECRET_KEY = '12345'

    ### Flask-security

    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha256_crypt'

    ### Pagination
   
