from connection import connectDB
from generator import generate_reference_no_CASHIN, generate_reference_no_SENDPAYMENT, generate_cashIN_date, generate_sendpayment_date
from admin import admin_bypass_code

REGISTERED_name = ""

class student:
    def __init__(self):
        self.fname = ""
        self.lname = ""
        self.student_id = 0
        self.email = ""
        self.contact_num = ""
        self.pin = 0
        self.course = ""
        self.year_lvl = 0
        self.balance = 0.0

class financial_status:
    def __init__(self):
        self.status_id = 0
        self.tuition_amtb = 0.0
        self.uniform_amtb = 0.0
        self.books_amtb = 0.0
        self.payment_status = ""
        self.discount_status = ""
        self.scholar_type = ""
        self.semester = ""
        self.purpose = ""

class payment_transac:
    def __init__(self):
        self.payment_id = 0
        self.ticket_id = 0
        self.status_id = 0
        self.payment_date = ""
        self.reference_no = ""
        self.payment_amount = 0.0

def main():
    while True:
        print("\n[INQUI-PAY]")
        print("1. Enter PIN")
        print("2. Register")
        print("3. Admin")
        print("4. Exit")
        try:
            choice = int(input("Enter: "))
        except ValueError:
            choice = -1
        match choice:
            case 1:
                login()
            case 2:
                regis()
            case 3:
                admin_bypass()
            case 4:
                exit()
            case _:
                for i in range(3):
                    print("\n[PLEASE ENTER A VALID INPUT]")


def regis():
    students = student()
    print("\n   [WELCOME TO REGISTRATION]")
    print("--- PLEASE ENTER THE FOLLOWING ---")
    students.fname = input("Enter your first name: ")
    students.lname = input("\nEnter your last name: ")
    students.course = input("\nEnter your course: ")
    students.year_lvl = input("\nEnter your year level: ")
    students.student_id = int(input("\nEnter your student id: "))
    students.email = input("\nEnter your email: ")
    students.contact_num = input("\nEnter your contact number: ")
    print("\n--- PLEASE CREATE A PIN ---")
    students.pin = input ("Create your pin: ")
    saveSTUDENTS(students)

def login():
    db = connectDB()
    cursor = db.cursor(dictionary=True)
    # SIMPLE LOG IN MENU
    print("\n[LOG - IN]")
    pin_LG = input("Enter your PIN: ")
    pin_query = "SELECT * FROM student WHERE pin = %s"
    cursor.execute(pin_query, (pin_LG,))
    result = cursor.fetchone()
    # BYPASSING TO THE MAIN MENU (INQUIPAY)
    if result:
        print("\n[LOG - IN SUCCESSFUL]")
        global REGISTERED_name
        REGISTERED_name = result['first_name']
        inquipay()
    else:
        print("\n[INVALID PIN]")

def admin_bypass():
    print("\n[ADMIN BYPASS MENU]")
    code = admin_bypass_code()
    try:
        bypass = float(input("Enter Admin Code: "))
    except ValueError:
        bypass = -1
    if bypass == code:
        admin()
    else:
        for i in range(3):
            print("\n[INVALID CODE]")

def admin():
    while True:
        print("\n[ADMIN PANELS]")
        print("1. Manage Tuition Fees Payments / Inquiries")
        print("2. Manage Uniform Payments / Inquiries")
        print("3. Manage Books Payments / Inquiries")
        print("4. Go Back")
        try:
            choice = int(input("Enter: "))
        except ValueError:
            choice = -1
        match choice:
            case 1:
                manageTUI()
            case 2:
                manageUNI()
            case 3:
                manageBOOKS()
            case 4:
                break
            case _:
                for i in range(3):
                    print("\n[PLEASE ENTER A VALID INPUT]")

def manageTUI():
    print("\n[MANAGE TUITION PAYMENTS AND INQUIRIES]")
    student_status = financial_status()

def inquipay():
    while True:
        print(f"\n[WELCOME {REGISTERED_name}]")
        print("1. Cash In")
        print("2. Send to Recipient")
        print("3. Pay School Requisites")
        print("4. Notifications")
        print("5. Check Balance")
        print("6. Help Center")
        try:
            choice = int(input("Enter: "))
        except ValueError:
            choice = -1
        match choice:
            case 1:
                cashIN()
            case 2:
                sendtoRECIPIENT()

def cashIN():
    stud_balance = student()
    print("\n[CASH IN]")
    stud_balance.balance = float(input("Enter Amount: "))
    saveSTUDENTS_BALANCE(stud_balance)

def sendtoRECIPIENT():
    transactions = payment_transac()
    print("\n[SEND TO RECIPIENT]")
    recipient_student_id = input("Enter Recipient's Student ID: ")
    transactions.payment_amount = float(input("\nEnter Amount to Send: "))
    saveSEND_RECIPIENT_PROCESS(recipient_student_id, transactions)

def saveSTUDENTS(students):
    my_sql = connectDB()
    cursor = my_sql.cursor()
    try:
        insert_student_data_query = """INSERT INTO student(student_id, first_name, last_name, course, year_level, email, contact_number, pin)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            students.student_id, students.fname, students.lname, students.course,
            students.year_lvl, students.email, students.contact_num, students.pin
        )
        cursor.execute(insert_student_data_query, values)
        print("\n[DATA SAVED]\n")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print("\n[DATA FAILED TO BE SAVED]", e)
    finally:
        my_sql.close()

def saveSTUDENTS_BALANCE(stud_balance):
    my_sql = connectDB()
    cursor = my_sql.cursor()
    try:
        update_student_balance_query = "UPDATE student SET balance = balance + %s WHERE first_name = %s"
        value = (stud_balance.balance, REGISTERED_name)
        cursor.execute(update_student_balance_query, value)
        cash_in_ref = generate_reference_no_CASHIN()
        cash_in_date = generate_cashIN_date()
        print(f"\n=== REFERENCE NO.: {cash_in_ref} ===")
        print(f"[Php {stud_balance.balance} WAS DEPOSITED IN YOUR ACCOUNT]")
        print(f"=== DATE: {cash_in_date} ===")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print(f"\n[CASH IN FAILED]", e)
    finally:
        my_sql.close()

def saveSEND_RECIPIENT_PROCESS(recipient_student_id, transactions):
    transactions.payment_date = generate_sendpayment_date()
    transactions.reference_no = generate_reference_no_SENDPAYMENT()
    my_sql = connectDB()
    cursor = my_sql.cursor(dictionary=True)
    try:
        query_sender = "SELECT * FROM student WHERE first_name = %s"
        cursor.execute(query_sender, (REGISTERED_name,))
        sender = cursor.fetchone()
        if sender is None:
            print("\n[USER DOES NOT EXIST]")
            return
        if sender['balance'] < transactions.payment_amount:
            print("\n[INSUFFICIENT FUNDS]")
            return
        query_receiver = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(query_receiver, (recipient_student_id,))
        receiver = cursor.fetchone()
        if receiver is None:
            print("\n[USER DOES NOT EXIST]")
            return
        transaction_sender = "UPDATE student SET balance = balance - %s WHERE student_id = %s"
        cursor.execute(transaction_sender, (transactions.payment_amount, sender['student_id']))
        transaction_receiver = "UPDATE student SET balance = balance + %s WHERE student_id = %s"
        cursor.execute(transaction_receiver, (transactions.payment_amount, recipient_student_id))
        insert_transaction = """INSERT INTO payment_transaction (ticket_id, sender_name, receiver_name, payment_amount, reference_no)
        VALUES (%s, %s, %s, %s)"""
        values = (sender['ticket_id'], sender['first_name'], receiver['first_name'], transactions.payment_amount, transactions.reference_no)
        cursor.execute(insert_transaction, values)
        print(f"\n=== REFERENCE NO.: {transactions.reference_no} ===")
        print(f"[SUCCESSFULLY SENT Php {transactions.payment_amount} to {receiver['first_name']}]")
        print(f"[YOUR CURRENT BALANCE: Php {float(sender['balance']) - transactions.payment_amount}]")
        print(f"=== DATE: {transactions.payment_date} ===")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print("\n[TRANSFER FAILED]", e)
    finally:
        my_sql.close()

if __name__ == "__main__":
    main()