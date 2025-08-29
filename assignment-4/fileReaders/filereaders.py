import json

with open("orders.json","r") as file:
    orders = json.load(file)

with open("faq.json","r") as file:
    faqs = json.load(file)