from Main import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(10), nullable=False)  # Add the year column
    user = db.relationship('User', backref='favorites', lazy=True)

    def __repr__(self):
        return f"Favorite('{self.title}', '{self.author}')"

class WantToRead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    user = db.relationship('User', backref='want_to_read', lazy=True)

    def __repr__(self):
        return f"WantToRead('{self.title}', '{self.author}')"

class ReadBefore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    user = db.relationship('User', backref='read_before', lazy=True)

    def __repr__(self):
        return f"ReadBefore('{self.title}', '{self.author}')"

class Clicked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    count = db.Column(db.Integer, default=1)
    user = db.relationship('User', backref='clicked', lazy=True)

    def __repr__(self):
        return f"ReadBefore('{self.title}', '{self.author}')"
