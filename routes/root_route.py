from flask import Blueprint, render_template, request
import os

bp = Blueprint('root', __name__, url_prefix='/root')


@bp.get('/')
def root():
	pk_key = os.urandom(12).hex()
	print(pk_key)
	return render_template('root_page.html', pk_key=pk_key)



