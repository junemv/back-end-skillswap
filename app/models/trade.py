from app import db


class Trade(db.Model):
    trade_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    send_user = db.Column(db.Integer, db.ForeignKey("user_.user_id"))
    recip_user = db.Column(db.Integer, db.ForeignKey("user_.user_id"))
    send_skill = db.Column(db.Integer, db.ForeignKey("skill.skill_id"))
    recip_skill = db.Column(db.Integer, db.ForeignKey("skill.skill_id"))
    send_accept = db.Column(db.Boolean)
    recip_accept = db.Column(db.Boolean)