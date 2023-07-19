from flask_admin.contrib.sqla import ModelView

from app import admin_app, db
from app.models import Mem, Tag, Account, Role

import os

from app.service import ImageService

admin_app.add_view(ModelView(Account, db.session))
admin_app.add_view(ModelView(Mem, db.session))
admin_app.add_view(ModelView(Tag, db.session))
admin_app.add_view(ModelView(Role, db.session))

# user_datastore = SQLAlchemyUserDatastore(db, Account, Role)
# security = Security(app, user_datastore)
#
#
# @security.context_processor
# def security_context_processor():
#     return dict(admin_base=admin_app.base_template,
#                 admin_view=admin_app.index_view,
#                 h=admin_helpers,
#                 get_url=url_for)


def find_link(filename):
    if Mem:
        mems = Mem.query.all()
        for mem in mems:
            if mem.link.split('/')[-1] == filename:
                return True
    return False


def remove_unnecessary_images():
    files = os.listdir(ImageService.IMG_PATH_DIR)
    basedir = os.path.abspath(os.path.dirname(__file__))
    try:
        for filename in files:
            if not find_link(filename) and not os.path.isdir(ImageService.IMG_PATH_DIR + filename):
                os.remove(os.path.join(basedir, ImageService.IMG_PATH + filename))
    except FileNotFoundError:
        print("Файла не существует")


remove_unnecessary_images()