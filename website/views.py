from flask import Blueprint as bp, flash, jsonify, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# define the file as a blueprint which will contain a bunch of roots/URL
views = bp('views', __name__)

# typing '/' in web address will go to the views which contains home. @login_required also have user to login before viewing homepage
@views.route('/', methods=['GET', 'POST'])
@login_required
def home(): 
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else: 
            # create Note object and add inputted note and current user's ID to record the ID that created the new note
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    # checks if user is 'authenticate' and define them as the current user
    return render_template("home.html", user=current_user)

# create event delete note to remove the note on a user
@views.route('/delete-note', methods=['POST'])
def delete_note():
    # get POST data and will reference index.json, especially the user's ID associated on creation of note
    # loaded as a json object or python dictionary
    note = json.loads(request.data)

    # access noteID attribute from index.json
    noteId = note['noteId']

    # search note with associated noteID
    note = Note.query.get(noteId)

    # check if note with associated ID exists
    if note:
        # check if signed in user's ID is the same ID associated with the note that will be deleted
        if note.user_id == current_user.id:
            # delete the note and update the database
            db.session.delete(note)
            db.session.commit()

    # return an empty response
    return jsonify({})