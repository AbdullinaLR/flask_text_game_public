from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class CharacterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    strength = IntegerField('Strength', validators=[DataRequired()])
    agility = IntegerField('Agility', validators=[DataRequired()])
    submit = SubmitField('Create Character')
