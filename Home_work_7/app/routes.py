from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Note

main = Blueprint('main', __name__)

@main.route('/')
def index():
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return render_template('index.html', notes=notes)

@main.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            new_note = Note(title=title, content=content)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('main.index'))
    return render_template('add.html')