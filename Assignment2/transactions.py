from random import choices, randint
from string import ascii_letters, digits
from faker import Faker
import sympy
count=0
import datetime
account_chars: str = digits
def _random_account_id() -> str:
    return "".join(choices(account_chars,k=3))
def _random_amount() -> float:
    return randint(10000,100000)
def _random_location(): 
    global count
    fake = Faker()
    Faker.seed(randint(1,1000))
    if(sympy.isprime(count)):
    	p=fake.location_on_land()
    else:	
    	p=fake.local_latlng(country_code='IN', coords_only=False)
    #print(type(p))
    l=[p[0],p[1],p[3]]
    count+=1
    return l
def _random_date():
	fake = Faker()
	start_date = datetime.date(year=2021, month=6, day=13)
	p=fake.date_time_between(start_date=start_date, end_date='now')
	dt_string = p.strftime("%d/%m/%Y %H:%M:%S")
	date=dt_string[:10]
	time=dt_string[11:]
	l=[date,time]
	return l
def _random_ip():
    fake=Faker()
    if(sympy.isprime(count)):
    	Faker.seed()
    else:
        Faker.seed(randint(1,1000))	
    l=fake.ipv4_public()
    return l           
def create_random_transaction() -> dict:
    """Create a fake randomised transaction."""
    return {
        "source":_random_account_id()
       ,"target":_random_account_id()
       ,"amount":_random_amount()
       ,"location":_random_location()
       ,"ip":_random_ip()
       ,"datetime":_random_date()
       ,"currency":"INR"
    }
