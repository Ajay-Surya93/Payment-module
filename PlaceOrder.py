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
@app.route('/subscription',methods=["POST"])
def subscription():
    con = util.connection()
    cursor=con.cursor()

    data = request.headers.get('Authorization')
    if not data or not data.startswith('Bearer '):
        return jsonify({'message': 'Missing or invalid Authorization header'}), 401
    
    token = data.split(' ')[1]
    payload = jwt.decode(token,'your_jwt_secret_key', algorithms=['HS256'])

    print("payload:",payload)

    userid=payload["userid"]
    amount=payload['amount']
    productid=payload['productid']

    client = razorpay.Client(auth=(key_id, key_secret))
    print("razorpay connection")

    order_data = {
    "amount": int(amount)*100,  
    "currency": "INR",
    "payment_capture": 1 }


    try:
        order = client.order.create(data=order_data)
        order_id=order["id"]

        query = "INSERT INTO details VALUES (%s, %s,%s,%s)"
        cursor.execute(query, (userid,order_id,amount,productid))
        con.commit()

        print("order is establish")
    except Exception as e:
        print("Error creating order:", e)

    payload={
            'userid': payload['userid'],
            'orderid':order_id,
            'productid':productid,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    print("token was gereated")

    return jsonify({'token': token,"order":order_id})
app.run(debug=True,port=8082)







