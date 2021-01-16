from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spam_users.db'

db = SQLAlchemy(app)


class SpamUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    phoneNumber = db.Column(db.String(50), unique=True)
    telemarketer = db.Column(db.String(50), unique=True)
    telecomProvider = db.Column(db.String(50), unique=False)

# Route to get all the spam users
@app.route('/api/v1/spam_users', methods=['GET'])
def get_all_users():

    users = SpamUser.query.all()
    output = []
    for user in users:
        spam_user_data = {}
        spam_user_data['username'] = user.username
        spam_user_data['phoneNumber'] = user.phoneNumber
        spam_user_data['telemarketer'] = user.telemarketer
        spam_user_data['telecomProvider'] = user.telecomProvider
        output.append(spam_user_data)
    return jsonify({'spam_users': output})

# Route to get insert new spam users
@app.route('/api/v1/insert_spam_user', methods=['POST'])
def create_user():
    data = request.get_json()

    new_spam_user = SpamUser(username=data['username'], phoneNumber=data['phoneNumber'], telemarketer=data['telemarketer'],telecomProvider=data['telecomProvider'] )
    db.session.add(new_spam_user)
    db.session.commit()

    return jsonify({"data": {"message": "User Successfully Created",
                             "isSuccess": "true", }, "code": "200"})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
