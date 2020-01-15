"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from RoyWebProject2_alternative import app

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
