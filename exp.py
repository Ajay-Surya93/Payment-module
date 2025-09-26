from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] ='your_jwt_secret_key'

# Route to generate token
@app.route('/login',methods=["POST"])
def login():
    data = request.args
    username = data.get('username')
    password = data.get('password')
    print(username)
    print(password)
    # Dummy check
    if username == 'admin' and password == 'password':
        payload={
            'amount': 500,
            "userid":12345,
            "productid":9456,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials'}), 401
app.run(debug=True,port=8081)