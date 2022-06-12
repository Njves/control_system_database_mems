from flask_admin.contrib.sqla import ModelView

from app import admin_app, db
from app.models import Mem, Tag, Account, mem_tag

admin_app.add_view(ModelView(Account, db.session))
admin_app.add_view(ModelView(Mem, db.session))
admin_app.add_view(ModelView(Tag, db.session))

