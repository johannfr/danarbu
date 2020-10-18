from danarbu import db


class Danarbu(db.Model):
    __tablename__ = "tbl_danarbu"
    id = db.Column(db.Integer, primary_key=True)
    nafn = db.Column(db.String(100))

    def __repr__(self):
        return "<Danarbu {}: {}".format(self.id, self.nafn)
