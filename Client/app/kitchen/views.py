from . import kitchen
from flask import render_template
from ..main.forms import Login
import random

@kitchen.route('/')
def index():
    return render_template('kitchen/index.html')


@kitchen.route('/orderInfo')
def orderInfo():
    info = open("app/templates/main/test.txt", 'r')
    line = "\n".join(info.readlines())
    info.close()
    return line
