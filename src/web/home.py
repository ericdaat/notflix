from flask import Blueprint, render_template
from web.db import db_session
from data_connector.models import Product


bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    products = db_session.query(Product).limit(10).all()
    return render_template('home/index.html', products=products)