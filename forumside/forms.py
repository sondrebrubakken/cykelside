from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from forumside.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',  validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email() ])
    password = PasswordField('Password', validators=[DataRequired(),])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use')    
        
        
        
class LoginForm(FlaskForm):
    username = StringField('Username',  validators=[DataRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired(),])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')
    
    

class MedlemForm(FlaskForm):
    navn = StringField('Navn',  validators=[DataRequired()], render_kw={"placeholder": "Navn"})
    email = StringField('Email', validators=[DataRequired(),Email() ], render_kw={"placeholder": "Email"})
    addresse = StringField('Addresse',  validators=[DataRequired()], render_kw={"placeholder": "Addresse"})
    postnummer = IntegerField('PostNummer', validators=[DataRequired(), Length(min=4, max=4)], render_kw={"placeholder": "Postnummer"})
    telefon = IntegerField('Telefon Nummer', validators=[DataRequired()], render_kw={"placeholder": "Telefon nummer"})
    fdato = DateField('Fødsels Dato', validators=[DataRequired()], render_kw={"placeholder": "Fødselsdato"})
    besked = TextAreaField('Besked')
    submit = SubmitField('Send Ind', validators=[DataRequired()])



class SubmitForm(FlaskForm):
    jylland = SubmitField('Jyllandsgade')
    badehus = SubmitField('Badehus vej')
    jomfru = SubmitField('Jomfru Ane Gade')
    pizza = SubmitField('Pizza')
    
    
class RuteForm(FlaskForm):
    route = StringField('iFrame link', validators=[DataRequired()])
    submit = SubmitField('Submit')