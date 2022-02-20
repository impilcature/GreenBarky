from asyncio.windows_events import NULL
from pickle import TRUE
from webbrowser import get
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null, true
from datetime import datetime
import logging
import time

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Bookmarks(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    title = db.Column("title", db.String(255), unique=True)
    url = db.Column("url", db.String(255))
    notes = db.Column("notes", db.Text)
    date_added = db.Column("date_added", db.DateTime)
    date_edited = db.Column("date_edited", db.DateTime)

    def __repr__(self):
        return '<Bookmarks %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        form_title = request.form['title']
        form_url = request.form['url'] 
        form_notes = request.form['note']

        new_bookmark = Bookmarks(
            title = form_title,
            url = form_url,
            notes = form_notes
            #date_added = time.strftime('%Y-%m-%d %H:%M:%S')
            #date_edited = null                
        )
        try:
            db.session.add(new_bookmark)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return 'There was an issue adding your bookmark'
            print(str(e))

            

    else:
        bookmarks = Bookmarks.query.order_by(Bookmarks.id).all()
        return render_template('index.html', bookmarks=bookmarks)

@app.route('/delete/<int:id>')
def delete(id):
    bookmark_to_delete = Bookmarks.query.get_or_404(id)

    try:
        db.session.delete(bookmark_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that bookmark'

"""
@app.route('/edit/<init:id>', methods=['GET', 'POST'])
def edit(id):
    bookmark = Bookmarks.query.get_or_404(id)
    
    if request.method == 'POST':
        bookmark.title = request.form['title']
        bookmark.url = request.form['url']
        bookmark.notes = request.form['notes']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your bookmark'

    else:
        return render_template('update.html', bookmark = bookmark)
"""

if __name__ == '__main__':
    app.debug = True
    app.run()