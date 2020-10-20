from danarbu import db
import enum


Kyn = enum.Enum(
    value="kyn",
    names=[
        ("KK", 1),
        ("KVK", 2),
        ("Hjón", 3),
        ("Hjon", 3),
    ],
)

Tilvist = enum.Enum(
    value="tilvist",
    names=[
        ("Til", 1),
        ("til", 1),
        ("Ekki Til", 2),
        ("ekki_til", 2),
        ("Loðs", 3),
        ("lods", 3),
    ],
)


class Danarbu(db.Model):
    __tablename__ = "tbl_danarbu"
    id = db.Column(db.Integer, primary_key=True)
    nafn = db.Column(db.String(100))
    stada = db.Column(db.String(200))
    kyn = db.Column(db.Enum(Kyn))
    aldur = db.Column(db.Integer)
    faeding = db.Column(db.String(45))
    andlat = db.Column(db.String(45))
    sysla_heiti = db.Column(db.String(45))
    sysla = db.Column(db.Integer)
    sokn_heiti = db.Column(db.String(45))
    sokn = db.Column(db.Integer)
    baer_heiti = db.Column(db.String(45))
    baer = db.Column(db.Integer)
    artal = db.Column(db.Integer)
    skipti = db.Column(db.String(50))
    skraning = db.Column(db.String(50))
    uppbod = db.Column("uppboð", db.String(45))
    mat = db.Column(db.Integer)
    lifandi = db.Column(db.Boolean)
    fannstAllsEkki = db.Column(db.Boolean)
    enginAldur = db.Column(db.Boolean)
    fannstEkki = db.Column(db.Boolean)
    leitAldur = db.Column(db.Boolean)
    danarbu = db.Column(db.Enum(Tilvist))
    skiptabok = db.Column(db.Enum(Tilvist))
    uppskrift = db.Column(db.Enum(Tilvist))
    athugasemdir = db.Column(db.String(5000))

    def __repr__(self):
        return "<Danarbu {}: {}>".format(self.id, self.nafn)


class Heimildir(db.Model):
    __tablename__ = "tbl_heimildir"
    id = db.Column(db.Integer, primary_key=True)
    danarbu = db.Column("id_danarbu", db.Integer, db.ForeignKey("tbl_danarbu.id"))
    upprunaleg = db.Column(db.String(100))
    endanleg = db.Column(db.String(100))
    tilvisun = db.Column(db.String(200))
    tegund = db.Column(db.String(100))


class Myndir(db.Model):
    __tablename__ = "tbl_myndir"
    id = db.Column(db.Integer, primary_key=True)
    slod = db.Column(db.String(2000))
    heimild = db.Column("id_heimild", db.Integer, db.ForeignKey("tbl_heimildir.id"))


class Hjalp(db.Model):
    __tablename__ = "tbl_hjalp"
    id = db.Column(db.Integer, primary_key=True)
    texti = db.Column(db.String(5000))


class Itarefni(db.Model):
    __tablename__ = "tbl_itarefni"
    id = db.Column(db.Integer, primary_key=True)
    texti = db.Column(db.String(5000))


class UmVefinn(db.Model):
    __tablename__ = "tbl_umvefinn"
    id = db.Column(db.Integer, primary_key=True)
    texti = db.Column(db.String(5000))
