from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, app
)
from werkzeug.exceptions import abort
import os

from werkzeug.utils import secure_filename

from flaskr import ALLOWED_EXTENSIONS

bp = Blueprint('morphing', __name__)


@bp.route('/')
def index():
    return render_template('morphing/index.html')
