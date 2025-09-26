import razorpay
from flask import Flask, request, jsonify
import jwt
import util
import datetime

key_id="rzp_test_RJLk2LeTUuq3Lc"
key_secret="FDc8XeclzLM0lJIg2Ie84bQt"
app = Flask(__name__)
app.config['SECRET_KEY'] ='your_jwt_secret_key'

# Route to generate token
@app.route('/verify',methods=["POST"])
def subscription():
    con = util.connection1()
    cursor=con.cursor()
    print(request.headers)
    data = request.headers.get('Authorization')
    if not data or not data.startswith('Bearer '):
        return jsonify({'message': 'Missing or invalid Authorization header'}), 401
    
    token = data.split(' ')[1]
    payload = jwt.decode(token,app.config['SECRET_KEY'], algorithms=['HS256'])

    print("payload:",payload)

    userid=payload["userid"]
    order_id=payload['orderid']
    productid=payload['productid']
    print("qurying")
    query = "INSERT INTO verify(userid,orderid) VALUES (%s, %s)"
    cursor.execute(query, (userid,order_id))
    con.commit()
    client = razorpay.Client(auth=(key_id, key_secret))
    print("razorpay connection")
    paymentid=request.args.get("paymentid")
    print(paymentid)
    try:
        payment = client.payment.fetch(paymentid)
    except Exception:
        return jsonify({"status":'failed'})
    status = payment.get('status')
    if status == 'captured':
        print("Payment was successful!")
        query = "INSERT INTO verify(status) VALUES (%s)"
        cursor.execute(query,('success'))
        con.commit()

        payload={
            'userid': payload['userid'],
            'orderid':order_id,
            'productid':productid,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        print("token was gereated")

        return jsonify({'token': token,"status":'success'})

    return jsonify({"status":'failed'})

app.run(debug=True,port=8083)
