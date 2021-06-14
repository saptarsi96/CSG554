from flask import Flask, Response, stream_with_context, render_template, json, url_for

from kafka import KafkaConsumer
from settings import *
import datetime
from ipaddress import IPv4Address
# create the flask object app
app = Flask(__name__)

def stream_template(template_name, **context):
    print('template name =',template_name)
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

def time_in_range(x):
    """Return true if x is in the range [start, end]"""
    start=datetime.time(23, 0, 0)
    end=datetime.time(5, 0, 0)
    date_time_obj = datetime.datetime.strptime(x[1], '%H:%M:%S')
    x=date_time_obj.time()
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
def checkip(ip):
    if((IPv4Address(ip) > IPv4Address('92.0.0.1')and((IPv4Address(ip) < IPv4Address('220.255.255.255'))))):
    	return True
    else:
    	return False	
	        
def is_suspicious(transaction: dict) -> bool:
    """Simple condition to determine whether a transaction is suspicious."""
    #'''transaction["amount"] >=5000 and transaction["location"][2]!='IN' and not''' 
    return (transaction["amount"] >=80000  or transaction["location"][2]!='IN') and time_in_range(transaction["datetime"])==True and checkip(transaction["ip"])==False

# this router will render the template named index.html and will pass the following parameters to it:
# title and Kafka stream
@app.route('/')
def index():
    def g():
        consumer = KafkaConsumer(
            TRANSACTIONS_TOPIC
            , bootstrap_servers=KAFKA_BROKER_URL
            , value_deserializer=lambda value: json.loads(value)
            ,
        )
        for message in consumer:
            transaction: dict = message.value
            topic = FRAUD_TOPIC if is_suspicious(transaction) else LEGIT_TOPIC
            print(topic, transaction)  # DEBUG
            yield topic, transaction

    return Response(stream_template('index.html', title='Fraud Detector / Kafka',data=g()))

if __name__ == "__main__":
   app.run(host="localhost" , debug=True)
