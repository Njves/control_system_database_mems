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

