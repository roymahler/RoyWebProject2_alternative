
### ----------------------------------------------------------- ###
### --- include all software packages and libraries needed ---- ###
### ----------------------------------------------------------- ###
from datetime  import datetime

from flask_wtf import FlaskForm
from wtforms   import StringField, SubmitField
from wtforms   import Form, BooleanField, PasswordField
from wtforms   import TextField, TextAreaField, SelectField, DateField
from wtforms   import validators, ValidationError

from wtforms.validators import DataRequired
from matplotlib.figure  import Figure
from os                 import path

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import base64
import io

import pandas            as pd
import numpy             as np
import matplotlib.pyplot as plt
### ----------------------------------------------------------- ###



## This class have the fields that are part of the Login form.
##   This form will get from the user a 'username' and a 'password' and sent to the server
##   to check if this user is authorised to continue
## You can see three fields:
##   the 'username' field - will be used to get the username
##   the 'password' field - will be used to get the password
##   the 'submit' button - the button the user will press to have the 
##                         form be "posted" (sent to the server for process)
class LoginFormStructure(FlaskForm):
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')



## This class have the fields of a registration form
##   This form is where the user can register himself. It will have sll the information
##   we want to save on a user (general information) and the username ans PW the new user want to have
## You can see three fields:
##   the 'FirstName' field - will be used to get the first name of the user
##   the 'LastName' field - will be used to get the last name of the user
##   the 'PhoneNum' field - will be used to get the phone number of the user
##   the 'EmailAddr' field - will be used to get the E-Mail of the user
##   the 'username' field - will be used to get the username
##   the 'password' field - will be used to get the password
##   the 'submit' button - the button the user will press to have the 
##                         form be "posted" (sent to the server for process)
class UserRegistrationFormStructure(FlaskForm):
    FirstName  = StringField('First name:  ' , validators = [DataRequired()])
    LastName   = StringField('Last name:  ' , validators = [DataRequired()])
    PhoneNum   = StringField('Phone number:  ' , validators = [DataRequired()])
    EmailAddr  = StringField('E-Mail:  ' , validators = [DataRequired()])
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Password:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')

##   This class have the fields that the user can set, to have the query parameters for analysing the data
##   This form is where the user can set different parameters
##   that will be used to do the data analysis (using Pandas etc.)
##   You can see two fields:
##   the 'submit' button - the button the user will press to have the 
##   form be "posted" (sent to the server for process)
# class DataParametersFormStructure(FlaskForm):
#    
# submit = SubmitField('Submit')


class DataQuery(FlaskForm):
    ShipName  = StringField('Ship Name:  ' , validators = [DataRequired()])
    ShipClass   = StringField('Warship Class:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')

    def plot_to_img(fig):
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return pngImageB64String