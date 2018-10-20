from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import re

from .auth import login_required
from .db import get_db

bp = Blueprint('home', __name__)