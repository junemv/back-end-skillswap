from app import db
from flask import abort, make_response

class Trade(db.Model):
    trade_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    send_user = db.Column(db.Integer, db.ForeignKey("user_.user_id"))
    recip_user = db.Column(db.Integer, db.ForeignKey("user_.user_id"))
    send_skill = db.Column(db.Integer, db.ForeignKey("skill.skill_id"))
    recip_skill = db.Column(db.Integer, db.ForeignKey("skill.skill_id"))
    send_accept = db.Column(db.Boolean)
    recip_accept = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime, nullable=True)
    send_viewed = db.Column(db.Boolean)
    recip_viewed = db.Column(db.Boolean)

    def to_json(self):
        return {
            "id": self.trade_id,
            "send_user": self.send_user,
            "recip_user": self.recip_user,
            "send_skill": self.send_skill,
            "recip_skill": self.recip_skill,
            "send_accept": self.send_accept,
            "recip_accept": self.recip_accept,
            "time_stamp": self.time_stamp,
            "send_viewed": self.send_viewed,
            "recip_viewed": self.recip_viewed
    }

    @classmethod
    def from_json(cls, trade_json):
        param_list = ["send_user", "recip_user", "send_skill", "recip_skill", "send_accept", "recip_accept", "send_viewed", "recip_viewed"]
        for param in param_list:
            if param not in trade_json.keys():
                return abort(make_response({"Invalid data": f"missing required item: {param}"}, 400))
        trade_json["time_stamp"] = None
        # may need to modify for teme_stamp if time_stamp is handled in back-end

        new_obj = cls(send_user=trade_json["send_user"], 
                    recip_user=trade_json["recip_user"], 
                    send_skill=trade_json["send_skill"], 
                    recip_skill=trade_json["recip_skill"],
                    send_accept=trade_json["send_accept"],
                    recip_accept=trade_json["recip_accept"],
                    time_stamp=trade_json["time_stamp"],
                    send_viewed=trade_json["send_viewed"],
                    recip_viewed=trade_json["recip_viewed"])

        return new_obj