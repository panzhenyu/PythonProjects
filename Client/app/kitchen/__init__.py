from flask import Blueprint

kitchen = Blueprint('kitchen', __name__)

from .views import *