from flask import Flask
from config import config_dict
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object(config_dict['config'])
db=SQLAlchemy(app)
import sys,os
from flask_uploads import IMAGES,UploadSet,configure_uploads
fn = getattr(sys.modules['__main__'], '__file__')
root_path = os.path.abspath(os.path.dirname(fn))+"/static/upload"

app.config['UPLOADED_PHOTO_DEST'] = root_path
app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES
photos = UploadSet('PHOTO')
configure_uploads(app, photos)