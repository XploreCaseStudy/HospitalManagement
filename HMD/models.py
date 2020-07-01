from datetime import datetime
from HMD import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.image_file}')"

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ws_pat_name = db.Column(db.String(100), nullable=False)
    ws_adrs = db.Column(db.String(100), nullable=False)
    ws_age = db.Column(db.String(10), nullable=False)
    ws_doj = db.Column(db.String(100), nullable=False)
    ws_rtype = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.id},{self.ws_pat_name}, {self.ws_adrs}, {self.ws_age},{self.ws_doj},{self.ws_rtype}"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"