total_price = 0
discount = 0
tax = 0

def set_price(price):
    global total_price
    total_price = price

def apply_discount(d):
    global discount, total_price
    discount = d
    total_price = total_price - discount

def apply_tax(t):
    global tax, total_price
    tax = t
    total_price = total_price + tax