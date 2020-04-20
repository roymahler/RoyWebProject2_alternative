"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from RoyWebProject2_alternative import app
from RoyWebProject2_alternative.models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError

from RoyWebProject2_alternative.models.QueryFormStracture import QueryFormStructure 
from RoyWebProject2_alternative.models.QueryFormStracture import LoginFormStructure
from RoyWebProject2_alternative.models.QueryFormStracture import UserRegistrationFormStructure
from RoyWebProject2_alternative.models.QueryFormStracture import DataQuery

##from RoyWebProject2_alternative.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser

db_Functions = create_LocalDatabaseServiceRoutines() 

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/project')
def project():
    """Renders the about page."""
    return render_template(
        'project.html',
        title='Project',
        year=datetime.now().year,
        message='My Project'
    )

@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            return redirect('/login')
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('/query')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/data')
def data():
    """Renders the about page."""
    return render_template(
        'data.html',
        title='Data',
        year=datetime.now().year,
        message='My Data'
    )

df = pd.read_csv("C:\\Users\\royma\\source\\repos\\RoyWebProject2_alternative\\RoyWebProject2_alternative\\RoyWebProject2_alternative\\static\\Data\\warships database.csv")
@app.route  ('/dataSet')
def dataSet():
    """Renders the about page."""
    return render_template(
        'dataSet.html',
        title='dataSet',
        year=datetime.now().year,
        message='My Data Set', data = df.to_html(classes = "table table-hover")
    )

@app.route('/query', methods=['GET', 'POST'])
def query():
    form = DataQuery(request.form)
    chart = " "
    table = " "

    if (request.method == 'POST' and form.validate()):  
        ShipName = form.ShipName.data
        ShipClass = form.ShipClass.data
        dfData = df.loc[df["Name"] == ShipName, "Type"].values[0]
        dfGroup = df.loc[df["Type"] == dfData]
        graph = plt.figure()
        plt.tight_layout()
        dfGroup.groupby("Warship Class")["Warship Class"].value_counts().plot(kind = 'barh', figsize=(15, 10), color = ['r' if sorted(dfGroup["Warship Class"].unique())[i] == ShipClass else 'b' for i in range(len(dfGroup["Warship Class"].unique()))])
        chart = DataQuery.plot_to_img(graph)
        table = dfGroup.to_html(classes="table table-hover")

    return render_template(
        'query.html',
        chart = chart,
        table = table,
        title='Query',
        form=form, 
        year=datetime.now().year,
        message='My Query'
    )
