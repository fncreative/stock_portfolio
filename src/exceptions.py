from . import app
from flask import render_template


@app.errorhandler(404)
def not_found(error):
    """Custom 404 Not Found handler.
    """
    return render_template('404_notfound.html', error=error), 404
