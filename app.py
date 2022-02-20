from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import true
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
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
        bookmark_content = request.form['bookmark']
        new_bookmark = Bookmarks(bookmark=bookmark_content)

        try:
            db.session.add(new_bookmark)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your bookmark'

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

@app.route('/update/<init:id>', methods=['POST', 'GET'])
def update(id):
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
        return render_template('update.html', bookmark_to_update = bookmark)



if __name__ == '__main__':
    app.debug = True
    app.run()