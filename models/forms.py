from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Optional

class CategoriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Guardar')


class UsuarioForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[Optional()])
    admin = BooleanField('Es administrador')
    submit = SubmitField('Guardar')
    
    
# forms.py
class DireccionForm(FlaskForm):
    usuario_id = IntegerField('ID Usuario', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    colonia = StringField('Colonia', validators=[DataRequired()])
    ciudad = StringField('Ciudad', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    codigo_postal = StringField('Código Postal', validators=[DataRequired()])
    pais = StringField('País', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    referencias = TextAreaField('Referencias')
    submit = SubmitField('Guardar')