import random
from datetime import datetime

def generate_reference_no_CASHIN():
    today = datetime.now().strftime("%Y%m%d")
    random_no = random.randint(100000, 999999)
    return f"INQ--{today}--{random_no}"

def generate_reference_no_SENDPAYMENT():
    today = datetime.now().strftime("%Y%m%d")
    random_no = random.randint(100000, 999999)
    return f"INQ--{today}--{random_no}"

def generate_cashIN_date():
    today = datetime.now().strftime("%B %d, %Y")
    return f"{today}"

def generate_sendpayment_date():
    today = datetime.now().strftime("%B %d, %Y")
    return f"{today}"