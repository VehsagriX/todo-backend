from flask import Flask, request
from resources import EntryManager, Entry

app = Flask(__name__)

FOLDER = 'C:/python_projects/todo-backend/project_notes/'


@app.route('/')
def hello_world():
    return '<p> Hello world!</p>'


@app.route('/api/entries/')
def get_entries():
    enty_manager = EntryManager(FOLDER)
    enty_manager.load()
    return [entry.json() for entry in enty_manager.entries]


@app.route('/api/save_entries/', methods=['POST'])
def save_entries():
    some_request = request.get_json()
    entry_manager = EntryManager(FOLDER)
    for item in some_request:
        entry = Entry.from_json(item)
        entry_manager.entries.append(entry)
    entry_manager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8000, debug= False)