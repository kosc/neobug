from flask import render_template

@neobug.route('/wiki/')
def index():
    return render_template('layout.html')
