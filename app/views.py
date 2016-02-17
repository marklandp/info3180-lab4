"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app
import os
from flask import session,flash,render_template, request, redirect, url_for
USERNAME="admin"
PASSWORD="naseberry"
SECRET_KEY="super secure key"

app.config.from_object(__name__)

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/files/')
def files():
    """files view"""
    if session['logged_in'] == True:
        return render_template("files.html")
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_entry():
    """add a file"""
    title = request.form['title']
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join("static/uploads", filename))
    return render_template("files.html",title=title)
    #g.db.execute('insert into entries (title, text) values (?, ?)',
    #             [title, filename])
    #g.db.commit()
    #flash('New entry was successfully posted')
    #return redirect(url_for('show_entries'))

@app.route('/login', methods=['POST','GET'])
def login():
    error = None 

    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username' 
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password' 
        else: 
            session['logged_in'] = True
            flash('You were logged in') 

    return render_template("login_form.html",error=error)

  
  
@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))
  
###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
