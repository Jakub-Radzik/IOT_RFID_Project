import datetime

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_mongoengine import MongoEngine

app = Flask(__name__)

DB_URI = "mongodb+srv://admin:admin@m001.hd4gnzi.mongodb.net/iot?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

db = MongoEngine(app)


# klasa do odzwierciedlenia obiektow w bazie


class logs(db.Document):
    log_id = db.IntField()
    date = db.DateTimeField()
    card_uid = db.StringField()
    reader = db.IntField()  # z ktorej raspberki przyszlo to do bazy

    def to_json(self):
        return {
            "log_id": self.log_id,
            "date": self.date,
            "card_uid": self.card_uid,
            "reader": self.reader
        }


@app.route("/logs/add", methods=['POST'])
def addLog():
    log_id = request.json.get("id", None)
    date = request.json.get("date", None)
    card_uid = request.json.get("card_uid", None)
    reader = request.json.get("reader", None)

    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')

    new_log = logs(log_id=log_id, date=date, card_uid=card_uid, reader=reader)
    new_log.save()

    return make_response("", 201)


@app.route("/logs/get", methods=['GET'])
def getLogs():
    all_logs = [log for log in logs.objects]
    return make_response(jsonify(all_logs), 200)

if __name__ == "__main__":
    app.run(debug=True)
