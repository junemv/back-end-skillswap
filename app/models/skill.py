from app import db


class Skill(db.Model):
    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tags = db.Column(db.ARRAY)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    skill_name = db.Column(db.String)
    description = db.Column(db.String)
    time = db.Column(db.Integer)