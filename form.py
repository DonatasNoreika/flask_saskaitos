from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField

class SaskaitaForm(FlaskForm):
    numeris = StringField('Numeris', [DataRequired()])
    balansas = IntegerField('Balansas')
    # vartotojas = QuerySelectField(query_factory=uzklausa)
    # vartotojas = SelectField('Vartotojas', choices=Vartotojas.query.all())
    # vartotojas = SelectField('Vartotojas', choices=[(1,"Group1"),(2,"Group2")], validators=[InputRequired])
    submit = SubmitField('Įvesti')

class VartotojasForm(FlaskForm):
    vardas = StringField('Numeris', [DataRequired()])
    pavarde = StringField('Pavardė', [DataRequired()])
    submit = SubmitField('Įvesti')