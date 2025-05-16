from flask import Flask, request
from model import db, Note
from flask_cors import CORS
from dotenv import load_dotenv
import os
from helper import send_response

load_dotenv()
app = Flask(__name__)
CORS(app,
     origins=["https://7d3tv6wg-5050.asse.devtunnels.ms/"],
     methods=["GET", "POST", "PUT", "DELETE"]
     )

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI_POSTGRE_CLOUD')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return send_response(200, 'go to /api')


@app.route("/api")
def test_api():
    return send_response(200, 'good boy')


@app.route("/api/notes", methods=['POST'])
def handle_post_note():
    if request.method != 'POST':
        send_response(400)

    body = request.get_json()
    if not body:
        return send_response(400, 'Bad Request')

    note_obj = {
        'note_id': body.get("note_id"),
        'note_title': body.get("note_title"),
        "note_description": body.get("note_description"),
        "note_type": body.get("note_type"),
        "created_at": body.get("created_at"),
    }
    new_note = Note(
        note_id=note_obj["note_id"],
        note_title=note_obj["note_title"],
        note_description=note_obj["note_description"],
        note_type=note_obj["note_type"],
        created_at=note_obj["created_at"],
    )
    try:
        db.session.add(new_note)
        db.session.commit()
    except:
        print('Failed to create note')
        return send_response(500, 'Failed to create Note')

    return send_response(201, 'Note created')


#### GET METHODS ####


@app.route("/api/notes", methods=['GET'])
def get_running_notes():
    note_type = request.args.get('note_type')
    notes = Note.query

    if note_type:
        if note_type != "all":
            notes = notes.filter(Note.note_type == note_type)
        else:
            notes = notes.order_by(
                Note.note_type == "urgent",
                Note.note_type == "important",
                Note.note_type == "regular"
            )
        # ^ kalo notesnya udh "done" nanti gaada tombol edit, delete atau done, vice versa
    else:
        notes = notes.all()

    if not notes:
        return send_response(200, [])

    result = [note.to_json() for note in notes]
    return send_response(200, result)


# @app.route("/api/notes", methods=['GET'])
# def get_number_of_notes(note_type):
#     body = request.get_json()
#     if not body:
#         return send_response(400, 'Bad Request')

#     note_type = body.get("note_type", default="all", type=str)

#     query = Note.query.filter(Note.note_type != "done",
#                               Note.note_type == note_type)
#     count = query.count()

#     return send_response(200, count)

#### DELETE METHODS #####
@app.route("/api/notes/<int:note_id>", methods=['DELETE'])
def delete_note(note_id):
    # body = request.get_json()
    if not note_id:
        return send_response(400, 'Bad Request')

    # note_id = body.get("note_id", default=0, type=int)
    note = Note.query.get(note_id)

    if not note:
        return send_response(404, 'Note not found')

    try:
        db.session.delete(note)
        db.session.commit()
    except:
        print('Failed to delete note')
        return send_response(500, 'Failed to delete Note')

    return send_response(200, 'Note deleted')

#### PUT METHODS ####


@app.route("/api/notes", methods=['PUT'])
def edit_note():
    body = request.get_json()
    if not body:
        return send_response(400, 'Bad Request')

    note_id = body.get("note_id")
    note_to_update = Note.query.get(note_id)
    if not note_to_update:
        return send_response(400, "Note not exist")

    note_obj = {
        'note_id': body.get("note_id"),
        'note_title': body.get("note_title"),
        "note_description": body.get("note_description"),
        "note_type": body.get("note_type"),
        "created_at": body.get("created_at"),
    }

    if 'note_title' in note_obj:
        note_to_update.title = note_obj["note_title"]
    if 'note_desc' in note_obj:
        note_to_update.title = note_obj["note_desc"]
    if 'note_type' in note_obj:
        note_to_update.title = note_obj["note_type"]

    try:
        db.session.commit()
    except:
        print('Failed to update note')
        return send_response(500, 'Failed to update Note')

    return send_response(201, 'Note updated')
    # body = request.get_json()
    # if not body:
    #     return send_response(400, 'Bad Request')
    # lgsg panggil aja note_id gausa body
    # ini mah harus panggil body ga sih, kan banyak gitu. kecuali masukin ke param semua?
    # iyaa kalo ini body aja


if __name__ == '__main__':
    app.run(debug=True, port=5050, host="0.0.0.0")
