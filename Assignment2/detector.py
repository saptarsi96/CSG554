import os
import json
import datetime
from kafka import KafkaConsumer, KafkaProducer
from ipaddress import IPv4Address
from settings import *
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
    return (transaction["amount"] >=80000  or transaction["location"][2]!='IN') and time_in_range(transaction["datetime"])==True and checkip(transaction["ip"])==False

if __name__ == "__main__":
   consumer = KafkaConsumer(
       TRANSACTIONS_TOPIC
      ,bootstrap_servers=KAFKA_BROKER_URL
      ,value_deserializer = lambda value: json.loads(value)
      ,
   )

   for message in consumer:
       transaction: dict = message.value
       topic = FRAUD_TOPIC if is_suspicious(transaction) else LEGIT_TOPIC
       print(topic,transaction) #DEBUG
