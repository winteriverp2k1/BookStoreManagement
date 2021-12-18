from myapp import app, db
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from myapp.models import Book, Author, Publisher, Book_Category, UserRole
from flask_login import current_user, logout_user
from flask import redirect


admin = Admin(app=app, name="ADMINISTRATION", template_mode='bootstrap4')

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)

class BookView(ModelView):
    can_view_details = True
    can_edit = True
    can_export = True
    column_searchable_list = ['name', 'type']
    column_filters = ['name', 'price']
    column_exclude_list = ['image', 'active', 'publish_date']
    column_labels = {
        'name': 'Ten SP',
        'book_category_id': 'Danh muc sach',
        'image': 'Anh dai dien',
        'type': 'The Loai',
        'price': 'Gia',
    }
    column_sortable_list = ['id', 'name', 'price']

class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(AuthenticatedModelView(Book, db.session))
admin.add_view(AuthenticatedModelView(Author, db.session))
admin.add_view(AuthenticatedModelView(Publisher, db.session))
admin.add_view(AuthenticatedModelView(Book_Category, db.session))
admin.add_view(LogoutView(name='Logout'))