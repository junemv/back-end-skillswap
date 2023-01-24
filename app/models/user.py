from app import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    city = db.Column(db.String)
    user_icon = db.Column(db.String)
    profile_desc = db.Column(db.String)