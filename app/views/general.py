from flask import render_template
from flask import Blueprint

general = Blueprint('general', __name__)

departments = [
    {
        'title': 'Development',
        'salary': 1500,
    },
    {
        'title': 'HR',
        'salary': 1400,
    }
]


@general.route('/')
def departments_page():
    return render_template('departments.html', title='Departments Page', departments=departments)


@general.route('/about')
def about_page():
    return render_template('about.html', title='About Page')
