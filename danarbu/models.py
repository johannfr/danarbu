from danarbu import db
import enum

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import ClauseElement, ColumnElement
from sqlalchemy import literal


class Match(ClauseElement):
    def __init__(self, columns, value):
        self.columns = columns
        self.value = literal(value)


@compiles(Match)
def _match(element, compiler, **kw):
    return "MATCH ({}) AGAINST ({} IN BOOLEAN MODE)".format(
        ", ".join(compiler.process(c, **kw) for c in element.columns),
        compiler.process(element.value),
    )


class MatchCol(ColumnElement):
    def __init__(self, columns, value):
        self.columns = columns
        self.value = literal(value)


@compiles(MatchCol)
def _match(element, compiler, **kw):
    return "MATCH ({}) AGAINST ({} IN BOOLEAN MODE)".format(
        ", ".join(compiler.process(c, **kw) for c in element.columns),
        compiler.process(element.value),
    )


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
        ("Loðs", 3),  # Bara notad af "danarbu", aldrei "skiptabok" eda "uppskrift"
        ("lods", 3),
    ],
)


class Danarbu(db.Model):
    __tablename__ = "danarbu_leit"
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
    danarbu = db.Column(db.Enum(Tilvist))
    skiptabok = db.Column(db.Enum(Tilvist))
    uppskrift = db.Column(db.Enum(Tilvist))
    athugasemdir = db.Column(db.String(5000))
    faeding_leit = db.Column(db.Integer)
    andlat_leit = db.Column(db.Integer)

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

    def __repr__(self):
        return "<Heimildir {}: {}>".format(self.id, self.danarbu)


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


class Tinyurl(db.Model):
    __tablename__ = "tinyurl"
    hashtime = db.Column(db.String(10), primary_key=True)
    obj = db.Column(db.String)
    visited = db.Column(db.Integer)
