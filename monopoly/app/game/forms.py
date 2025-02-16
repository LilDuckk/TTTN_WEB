from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class JoinGameForm(FlaskForm):
    join_code = StringField('Join Code', validators=[DataRequired()])
    submit = SubmitField('Join')
