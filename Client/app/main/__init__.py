from flask import Blueprint, redirect

main = Blueprint('main', __name__)

from .views import *
