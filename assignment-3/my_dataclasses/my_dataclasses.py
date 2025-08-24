from pydantic import BaseModel

class Hotel(BaseModel):
    name:str
    location:str
    rooms:int
    facilities:list
    price_per_night:int

floe = Hotel(name="Floe",location="Karachi",rooms=200,facilities=["4 swimming pools","4 gyms","free wi-fi"],price_per_night=15000)
moon = Hotel(name="Moon",location="Karachi",rooms=290,facilities=["7 swimming pools","9 gyms","breakfast buffet"],price_per_night=18000)
Jasmine = Hotel(name="Jasmine",location="Islamabad",rooms=180,facilities=["6 swimming pools","5 gyms","breakfast buffet","sea view"],price_per_night=17000)
royal = Hotel(name="Royal",location="lahore",rooms=250,facilities=["3 swimming pools","4 gyms","free wi-fi"],price_per_night=16000)
ballerina =  Hotel(name="Ballerina",location="Islamabad",rooms=300,facilities=["8 swimming pools","6 gyms","Traditional cusines","spa"],price_per_night=22000)

class User_info(BaseModel):
    name:str
    age:int
    email:str

user = User_info(name="John",age=24,email="john@gmail.com")