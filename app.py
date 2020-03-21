from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField

# https://www.youtube.com/watch?v=b9W2ul2VRRc

# https://youtu.be/u0oDDZrDz9U

# deploy
# https://youtu.be/goToXTC96Co

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
# from form import SaskaitaForm, VartotojasForm

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfgsfdgsdfgsdfgsdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'saskaitos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Saskaita(db.Model):
    __tablename__ = 'saskaitos'
    id = db.Column(db.Integer, primary_key=True)
    numeris = db.Column(db.String(80), nullable=False)
    balansas = db.Column(db.Float, nullable=False)
    vartotojas_id = db.Column(db.Integer, db.ForeignKey('vartotojai.id'))
    vartotojas = db.relationship("Vartotojas")


class Vartotojas(db.Model):
    __tablename__ = 'vartotojai'
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column(db.String(80), nullable=False)
    pavarde = db.Column(db.String(80), nullable=False)
    saskaitaos = db.relationship("Saskaita")

@app.route("/")
def invoices():
    try:
        visos_saskaitos = Saskaita.query.all()
    except:
        visos_saskaitos = []
    return render_template("saskaitos.html", visos_saskaitos=visos_saskaitos)

@app.route("/users")
def users():
    try:
        visi_vartotojai = Vartotojas.query.all()
    except:
        visi_vartotojai = []
    return render_template("vartotojai.html", visi_vartotojai=visi_vartotojai)

@app.route("/add_invoice", methods=["GET", "POST"])
def new_invoice():
    db.create_all()
    forma = SaskaitaForm()
    if forma.validate_on_submit():
        nauja_saskaita = Saskaita(numeris=forma.numeris.data, balansas=forma.balansas.data, vartotojas=forma.vartotojas.data)
        db.session.add(nauja_saskaita)
        db.session.commit()
        return invoices()
    return render_template("prideti_saskaita.html", form=forma)

@app.route("/add_user", methods=["GET", "POST"])
def new_user():
    db.create_all()
    forma = VartotojasForm()
    if forma.validate_on_submit():
        naujas_vartotojas = Vartotojas(vardas=forma.vardas.data, pavarde=forma.pavarde.data)
        db.session.add(naujas_vartotojas)
        db.session.commit()
        return redirect(url_for('users'))
    return render_template("prideti_vartotoja.html", form=forma)

def new_query():
    return Vartotojas.query

def get_pk(obj):
    return str(obj)

class SaskaitaForm(FlaskForm):
    numeris = StringField('Numeris', [DataRequired()])
    balansas = IntegerField('Balansas')
    vartotojas = QuerySelectField(query_factory=new_query, allow_blank=True, get_label="vardas", get_pk=get_pk)
    # vartotojas = SelectField('Vartotojas', choices=Vartotojas.query.all())
    # vartotojas = SelectField('Vartotojas', choices=[(1,"Group1"),(2,"Group2")], validators=[InputRequired])
    submit = SubmitField('Įvesti')

class VartotojasForm(FlaskForm):
    vardas = StringField('Numeris', [DataRequired()])
    pavarde = StringField('Pavardė', [DataRequired()])
    submit = SubmitField('Įvesti')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
    db.create_all()