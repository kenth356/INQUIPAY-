from connection import connectDB
import generator
from adminCODE import admin_inquipay
import random

REGISTERED_name = ""
REGISTERED_studentID = 0

class student:
    def __init__(self):
        self.student_id = 0
        self.pin = 0
        self.fname = ""
        self.lname = ""
        self.email = ""
        self.contact_num = ""
        self.course = ""
        self.year_lvl = 0
        self.balance = 0.0

class financial_status:
    def __init__(self):
        self.status_id = 0
        self.payment_status = ""
        self.discount_type = ""
        self.semester = ""
        self.purpose = ""
        self.status_column = ""
        self.new_status = ""
        self.tuition_amtb = 0.0
        self.uniform_amtb = 0.0
        self.books_amtb = 0.0
        self.total_amtb = 0.0
        self.discount_percent = 0.0
        self.final_amtb = 0.0
        self.amount_due = 0.0

class payment_transac:
    def __init__(self):
        self.payment_id = 0
        self.ticket_id = 0
        self.status_id = 0
        self.payment_date = ""
        self.reference_no = ""
        self.payment_amount = 0.0
        self.purpose = ""

class notifications:
    def __init__(self):
        self.notif_id = 0
        self.notif_type = ""
        self.notif_message = ""
        self.notif_date = ""

class discounted_fees:
    def __init__(self):
        self.tuition_discounted = 0.0
        self.book_discounted = 0.0
        self.uniform_discounted = 0.0
        self.total_discounted = 0.0
        self.discounts = None

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

def inquipay():
    while True:
        print(f"\n[WELCOME {REGISTERED_name}]")
        print("1. Cash In")
        print("2. Send to Recipient")
        print("3. Pay School Requisites")
        print("4. Notifications")
        print("5. Check Balance")
        print("6. Help Center")
        print("7. Go Back")
        try:
            choice = int(input("Enter: "))
        except ValueError:
            choice = -1
        match choice:
            case 1:
                cashIN()
            case 2:
                sendtoRECIPIENT()
            case 3:
                paytoSCHOOLREQ()
            case 4:
                viewNOTIFS()
            case 5:
                checkBALANCE()
            case 6:
                helpCENTER()
            case 7:
                break
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
        global REGISTERED_name, REGISTERED_studentID
        REGISTERED_name = result['first_name']
        REGISTERED_studentID = result['student_id']
        inquipay()
    else:
        print("\n[INVALID PIN]")

def admin_bypass():
    print("\n[ADMIN BYPASS MENU]")
    code = admin_inquipay().admin_code
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
        print("1. Manage Tuition Fee")
        print("2. Manage Inquiries")
        print("3. Go back")
        try:
            choice = int(input("Enter: "))
        except ValueError:
            choice = -1
        match choice:
            case 1:
                manageTUI()
            case 2:
                manageINQ()
            case 3:
                break
            case _:
                for i in range(3):
                    print("\n[PLEASE ENTER A VALID INPUT]")

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
    transactions.purpose = input("\nEnter purpose: ")
    saveSEND_RECIPIENT_PROCESS(recipient_student_id, transactions)

def paytoSCHOOLREQ():
    transactions = payment_transac()
    print("\n[PAY SCHOOL REQUISITES]")
    transactions.purpose = input("Enter payment purpose: ")
    transactions.payment_amount = float(input("\nEnter Amount to Pay: "))
    savePAY_TO_SCHOOLREQ_PROCESS(transactions)

def viewNOTIFS():
    try:
        my_sql = connectDB()
        cursor = my_sql.cursor(dictionary=True)
        notification_query = "SELECT * FROM notifications WHERE student_id = %s ORDER BY notif_date DESC"
        cursor.execute(notification_query, (REGISTERED_studentID,))
        notifications_data = cursor.fetchall()
        if not notifications_data:
            print("\n[NO NEW NOTIFICATIONS]")
            return
        print("\n=== [NOTIFICATIONS] ===")
        for notifs in notifications_data:
            print(f"\n{notifs['notif_type'].upper()} || {notifs['notif_message']}")
            print(f"Date: {notifs['notif_date']}")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print("\n[FAILED TO LOAD NOTIFICATIONS]", e)

def checkBALANCE():
    my_sql = connectDB()
    cursor = my_sql.cursor(dictionary=True)
    check_balance_query = "SELECT * FROM student WHERE student_id = %s"
    cursor.execute(check_balance_query, (REGISTERED_studentID,))
    student_data = cursor.fetchone()
    if student_data is None:
        print("\n[STUDENT DATA DOES NOT EXISTS]")
    print(f"\n=== [YOUR CURRENT BALANCE: {student_data['balance']}]")

def helpCENTER():
    while True:
        print("\n[HELP CENTER]")
        print("1. Inquire to School")
        print("2. How to Use")
        print("3. Go Back")
        try:
            choice = int(input("Enter: "))
        except ValueError:
            choice = -1
        match choice:
            case 1:
                inquire()
            case 2:
                howtoUSE()
            case 3:
                break
            case _:
                for i in range(3):
                    print("\n[PLEASE ENTER A VALID INPUT]")

def inquire():
    print("\n[INQUIRE TO DYCI]")
    question = input("Enter inquiry: ")
    if "finance" in question.lower() and "open" in question.lower():
        is_open = random.choice([True, False])
        if is_open:
            print("\n[RESPONSE: Yes! DYCI Elida Campus is Open today for Financial Operations!]")
        else:
            print("\n[RESPONSE: DYCI is Closed today]")
    elif "statement of account" in question.lower() or "soa" in question.lower():
        reqSOA()
    elif "books" in question.lower() or "book" in question.lower():
        has_stock = random.choice([True, False])
        if has_stock:
            print("\n[RESPONSE: Yes! DYCI Elida Campus currently has book stocks available!]")
        else:
            print("\n[RESPONSE: DYCI Elida Campus book stocks are currently unavailable]")
    elif "uniform" in question.lower():
        has_stock = random.choice([True, False])
        if has_stock:
            print("\n[RESPONSE: Yes! DYCI Elida Campus currently has uniform stocks available!]")
        else:
            print("\n[RESPONSE: DYCI Elida Campus uniform stocks are currently unavailable]")
    else:
        print("\n[RESPONSE: Please do contact dycifinance@gmail.com For specific questions]")

def howtoUSE():
    print("\n[WELCOME TO INQUI-PAY HELP MANUAL!]")
    print("--------------------------------------")
    print("CASH-IN - Add funds in your account")
    print("SEND TO RECIPIENT - Send money to another inqui-pay user (student only)")
    print("PAY SCHOOL REQUISITES - Pay tuition, books, and uniforms!")
    print("NOTIFICATIONS - View system and school updates")
    print("CHECK BALANCE - View your current balance")
    print("HELP CENTER - Can inquire for school purpose and Help Manual")

def reqSOA():
    my_sql = connectDB()
    cursor = my_sql.cursor(dictionary=True)
    try:
        student_query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(student_query, (REGISTERED_studentID,))
        student_data = cursor.fetchone()
        if student_data is None:
            print("\n[STUDENT DATA NOT FOUND]")
            return
        financial_query = "SELECT * FROM financial_status WHERE ticket_id = %s"
        cursor.execute(financial_query, (student_data['ticket_id'],))
        finance_data = cursor.fetchone()
        if finance_data is None:
            print("\n[FINANCE DATA NOT FOUND]")
            return
        discount_query = "SELECT * FROM discounted_fees WHERE status_id = %s"
        cursor.execute(discount_query, (finance_data['status_id'],))
        discounted = cursor.fetchone()
        print("\n[STATEMENT OF ACCOUNT]")
        print(f"STUDENT NAME: {student_data['last_name']}, {student_data['first_name']}")
        print(f"STUDENT ID: {student_data['student_id']}")
        print("---------------------------------------------")
        print(f"ORIGINAL TUITION FEE: PHP {finance_data['tuition_amtb']}")
        print(f"ORIGINAL BOOKS FEE: PHP {finance_data['books_amtb']}")
        print(f"ORIGINAL UNIFORM FEE: PHP {finance_data['uniform_amtb']}")
        print(f"ORIGINAL TOTAL: PHP {finance_data['total_amtb']}")
        print("---------------------------------------------")
        if discounted:
            print(f"DISCOUNTED TUITION FEE: PHP {discounted['tuition_discounted']}")
            print(f"DISCOUNTED BOOKS FEE: PHP {discounted['books_discounted']}")
            print(f"DISCOUNTED UNIFORM FEE: PHP {discounted['uniform_discounted']}")
            print(f"DISCOUNTED TOTAL: PHP {discounted['total_discounted']}")
            print("----------------------------------------------")
        print(f"FINAL AMOUNT TO BE PAID: PHP {finance_data['final_amtb']}")
        print(f"PAYMENT STATUS: {finance_data['payment_status']}")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print("REQUESTING FAILED", e)
    finally:
        my_sql.close()

def manageTUI():
    student_status = financial_status()
    print("\n[MANAGE TUITION FEE PAYMENTS AND INQUIRIES]")
    student_id = int(input("Enter Student ID: "))
    student_status.tuition_amtb = float(input("\nEnter Tuition Fee Amount: "))
    student_status.uniform_amtb = float(input("\nEnter Uniform Amount: "))
    student_status.books_amtb = float(input("\nEnter Books Amount: "))
    student_status.discount_type = input("\nEnter Discount Type: ")
    student_status.semester = input("\nEnter Semester: ")
    saveTUISTAT(student_id, student_status)

def manageINQ():
    while True:
        print("\n[MANAGE INQUIRIES]")
        print("1. Toggle tuition notifications")
        print("2. Toggle uniform notifications")
        print("3. Toggle books notiifcations")
        print("4. Toggle system notifications")
        print("5. Go Back")
        try:
            choice = int(input("Enter: "))
        except ValueError:
            choice = -1
        match choice:
            case 1:
                tuitionNOTIFS()
            case 2:
                uniformNOTIFS()
            case 3:
                booksNOTIFS()
            case 4:
                systemNOTIFS()
            case 5:
                break
            case _:
                for i in range(3):
                    print("\n[PLEASE ENTER A VALID INPUT]")

def tuitionNOTIFS():
    notify = notifications()
    my_sql = connectDB()
    cursor = my_sql.cursor(dictionary=True)
    try:
        print("\n[TUITION NOTIFICATION PANEL]")
        student_id = int(input("Enter Student's SID: "))
        student_query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(student_query, (student_id,))
        student_data = cursor.fetchone()
        if student_data is None:
            print("\n[STUDENT NOT FOUND]")
            return
        student_schoolREQ_status_query = "SELECT * FROM financial_status WHERE ticket_id = %s"
        cursor.execute(student_schoolREQ_status_query, (student_data['ticket_id'],))
        student_schoolREQ_status_data = cursor.fetchone()
        if student_schoolREQ_status_data is None:
            print("\n[DATA NOT FOUND]")
        notify.notif_message = f"Hello, {student_data['first_name']}! Your tuition fee balance of Php {student_schoolREQ_status_data['final_amtb']}"
        insert_notify_query = """INSERT INTO notifications (student_id, notif_type, notif_message)
        VALUES (%s, %s, %s)"""
        values = (student_data['student_id'], "Tuition Fee", notify.notif_message)
        cursor.execute(insert_notify_query, values)
        print("\n[NOTIFICATION SENT!]")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print("\n[FAILED TO TOGGLE NOTIFICATION]", e)
    finally:
        my_sql.close()

def uniformNOTIFS():
    notify = notifications()
    my_sql = connectDB()
    cursor = my_sql.cursor(dictionary=True)
    try:
        print("\n[TUITION NOTIFICATION PANEL]")
        student_id = int(input("Enter Student's SID: "))
        student_query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(student_query, (student_id,))
        student_data = cursor.fetchone()
        if student_data is None:
            print("\n[STUDENT NOT FOUND]")
            return
        notify.notif_message = f"Hello, {student_data['first_name']}! School Uniforms now have Stocks at Elida Campus!"
        insert_notify_query = """INSERT INTO notifications (student_id, notif_type, notif_message)
        VALUES (%s, %s, %s)"""
        values = (student_data['student_id'], "Uniform", notify.notif_message)
        cursor.execute(insert_notify_query, values)
        print("\n[NOTIFICATION SENT!]")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print("\n[FAILED TO TOGGLE NOTIFICATION]", e)
    finally:
        my_sql.close()

def booksNOTIFS():
    notify = notifications()
    my_sql = connectDB()
    cursor = my_sql.cursor(dictionary=True)
    try:
        print("\n[TUITION NOTIFICATION PANEL]")
        student_id = int(input("Enter Student's SID: "))
        student_query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(student_query, (student_id,))
        student_data = cursor.fetchone()
        if student_data is None:
            print("\n[STUDENT NOT FOUND]")
            return
        notify.notif_message = f"Hello, {student_data['first_name']}! Books now have Stocks at Elida Campus!"
        insert_notify_query = """INSERT INTO notifications (student_id, notif_type, notif_message)
        VALUES (%s, %s, %s)"""
        values = (student_data['student_id'], "Books", notify.notif_message)
        cursor.execute(insert_notify_query, values)
        print("\n[NOTIFICATION SENT!]")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print("\n[FAILED TO TOGGLE NOTIFICATION]", e)
    finally:
        my_sql.close()

def systemNOTIFS():
    notify = notifications()
    my_sql = connectDB()
    cursor = my_sql.cursor(dictionary=True)
    try:
        print("\n[TUITION NOTIFICATION PANEL]")
        student_id = int(input("Enter Student's SID: "))
        student_query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(student_query, (student_id,))
        student_data = cursor.fetchone()
        if student_data is None:
            print("\n[STUDENT NOT FOUND]")
            return
        notify.notif_message = f"Hello, {student_data['first_name']}! Thank You So Much for Using INQUI-PAY!"
        insert_notify_query = """INSERT INTO notifications (student_id, notif_type, notif_message)
        VALUES (%s, %s, %s)"""
        values = (student_data['student_id'], "Appreciation", notify.notif_message)
        cursor.execute(insert_notify_query, values)
        print("\n[NOTIFICATION SENT!]")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print("\n[FAILED TO TOGGLE NOTIFICATION]", e)
    finally:
        my_sql.close()

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
        update_student_balance_query = "UPDATE student SET balance = balance + %s WHERE student_id = %s"
        value = (stud_balance.balance, REGISTERED_studentID)
        cursor.execute(update_student_balance_query, value)
        cash_in_ref = generator.generate_reference_no_CASHIN()
        cash_in_date = generator.generate_cashIN_date()
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
    transactions.payment_date = generator.generate_sendpayment_date()
    transactions.reference_no = generator.generate_reference_no_SENDPAYMENT()
    my_sql = connectDB()
    cursor = my_sql.cursor(dictionary=True)
    try:
        sender_query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(sender_query, (REGISTERED_studentID,))
        sender = cursor.fetchone()
        if sender is None:
            print("\n[USER DOES NOT EXIST]")
            return
        if sender['balance'] < transactions.payment_amount:
            print("\n[INSUFFICIENT FUNDS]")
            return
        receiver_query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(receiver_query, (recipient_student_id,))
        receiver = cursor.fetchone()
        if receiver is None:
            print("\n[USER DOES NOT EXIST]")
            return
        transaction_sender = "UPDATE student SET balance = balance - %s WHERE student_id = %s"
        cursor.execute(transaction_sender, (transactions.payment_amount, sender['student_id']))
        transaction_receiver = "UPDATE student SET balance = balance + %s WHERE student_id = %s"
        cursor.execute(transaction_receiver, (transactions.payment_amount, recipient_student_id))
        insert_transaction = """INSERT INTO payment_transaction (ticket_id, sender_name, receiver_name, payment_amount, purpose, reference_no)
        VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (sender['ticket_id'], sender['first_name'], receiver['first_name'], transactions.payment_amount, transactions.purpose, transactions.reference_no)
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

def savePAY_TO_SCHOOLREQ_PROCESS(transactions):
    finance = financial_status()
    transactions.payment_date = generator.generate_schoolREQS_date()
    transactions.reference_no = generator.generate_reference_no_SCHOOLREQS()
    my_sql = connectDB()
    cursor = my_sql.cursor(dictionary=True)
    try:
        student_query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(student_query, (REGISTERED_studentID,))
        student_data = cursor.fetchone()
        if not student_data:
            print("\n[USER DOES NOT EXIST]")
            return
        if student_data['balance'] < transactions.payment_amount:
            print("\n[INSUFFICIENT FUNDS]")
            return
        student_schoolREQ_query = "SELECT * FROM financial_status WHERE ticket_id = %s"
        cursor.execute(student_schoolREQ_query, (student_data['ticket_id'],))
        student_schoolREQ_data = cursor.fetchone()
        if not student_schoolREQ_data:
            print("\n[NO RECORD FOUND]")
            return
        student_transaction_query = "UPDATE student SET balance = balance - %s WHERE student_id = %s"
        cursor.execute(student_transaction_query, (transactions.payment_amount, REGISTERED_studentID))
        discount_query = "SELECT * FROM discounted_fees WHERE status_id = %s"
        cursor.execute(discount_query, (student_schoolREQ_data['status_id'],))
        discounted = cursor.fetchone()
        if discounted:
            if "tuition" in transactions.purpose.lower():
                finance.status_column = "tuition_status"
                finance.amount_due = float(discounted['tuition_discounted'])
            elif "books" in transactions.purpose.lower():
                finance.status_column = "books_status"
                finance.amount_due = float(discounted['books_discounted'])
            elif "uniform" in transactions.purpose.lower():
                finance.status_column = "uniform_status"
                finance.amount_due = float(discounted['uniform_discounted'])
            else:
                print("\n[INVALID PURPOSE]")
                return
        else:
            if "tuition" in transactions.purpose.lower():
                finance.status_column = "tuition_status"
                finance.amount_due = float(student_schoolREQ_data['tuition_amtb'])
            elif "books" in transactions.purpose.lower():
                finance.status_column = "books_status"
                finance.amount_due = float(student_schoolREQ_data['books_amtb'])
            elif "uniform" in transactions.purpose.lower():
                finance.status_column = "uniform_status"
                finance.amount_due = float(student_schoolREQ_data['uniform_amtb'])
            else:
                print("\n[INVALID PURPOSE]")
                return
        get_paid_query = "SELECT SUM(payment_amount) AS total_paid FROM payment_transaction WHERE ticket_id = %s and purpose = %s"
        cursor.execute(get_paid_query, (student_data['ticket_id'], transactions.purpose))
        paid = float(cursor.fetchone()['total_paid'] or 0)
        remaining_due = finance.amount_due - paid - transactions.payment_amount
        if remaining_due <= 0:
            finance.new_status = "APPROVED"
        else:
            finance.new_status = "PENDING"
        update_financial_stat_query = f"UPDATE financial_status SET {finance.status_column} = %s WHERE status_id = %s"
        cursor.execute(update_financial_stat_query, (finance.new_status, student_schoolREQ_data['status_id']))
        status_query = "SELECT tuition_status, books_status, uniform_status FROM financial_status WHERE status_id = %s"
        cursor.execute(status_query, (student_schoolREQ_data['status_id'],))
        student_finance_data = cursor.fetchone()
        if all(status == "APPROVED" for status in student_finance_data.values()):
            finance.payment_status = "PAID"
        elif any(status == "PENDING" for status in student_finance_data.values()):
            finance.payment_status = "SEMI-PAID"
        elif any(status == "APPROVED" for status in student_finance_data.values()):
            finance.payment_status = "SEMI-PAID"
        update_status_query = "UPDATE financial_status SET payment_status = %s WHERE status_id = %s"
        cursor.execute(update_status_query, (finance.payment_status, student_schoolREQ_data['status_id']))
        insert_payment_query = """INSERT INTO payment_transaction (ticket_id, status_id, payment_amount, purpose, reference_no,
        sender_name, receiver_name) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_payment_query, (student_data['ticket_id'], student_schoolREQ_data['status_id'], transactions.payment_amount, transactions.purpose, transactions.reference_no, REGISTERED_name, "DYCI Elida Finance"))
        print("\n=== [PAYMENT SUCCESSFUL] ===")
        print(f"REFERENCE NO.: {transactions.reference_no}")
        print(f"PURPOSE OF PAYMENT: {transactions.purpose}")
        print(f"AMOUNT PAID: Php {transactions.payment_amount}")
        print(f"STATUS: {finance.new_status}")
        print(f"[YOUR CURRENT BALANCE: {float(student_data['balance']) - transactions.payment_amount}]")
        print(f"=== DATE: {transactions.payment_date} ===")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print("\n[PAYMENT FAILED]", e)
    finally:
        my_sql.close()

def saveTUISTAT(student_id, student_status):
    discounts = discounted_fees()
    my_sql = connectDB()
    cursor = my_sql.cursor(dictionary=True)
    student_status.discount_percent = get_discount_rate(student_status.discount_type)
    student_status.total_amtb = student_status.tuition_amtb + student_status.uniform_amtb + student_status.books_amtb
    if student_status.discount_type and student_status.discount_percent > 0:
        discount_amount = (student_status.total_amtb * student_status.discount_percent) / 100
        student_status.final_amtb = student_status.total_amtb - discount_amount
        discounts.tuition_discounted = student_status.tuition_amtb - (student_status.tuition_amtb * student_status.discount_percent / 100)
        discounts.book_discounted = student_status.books_amtb - (student_status.books_amtb * student_status.discount_percent / 100)
        discounts.uniform_discounted= student_status.uniform_amtb - (student_status.uniform_amtb * student_status.discount_percent / 100)
        discounts.total_discounted = discounts.tuition_discounted + discounts.book_discounted + discounts.uniform_discounted
    else:
        student_status.discount_type = None
        student_status.discount_percent = 0.0
        student_status.final_amtb = student_status.total_amtb
        discounts = None
    try:
        get_ticketID_query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(get_ticketID_query, (student_id,))
        get_ticketID = cursor.fetchone()
        if get_ticketID is None:
            print("\n[RECORD NOT FOUND]")
            return
        financial_status_query = """INSERT INTO financial_status (ticket_id, tuition_amtb, uniform_amtb, books_amtb, total_amtb,
        discount_type, discount_percent, final_amtb, semester)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (get_ticketID['ticket_id'], student_status.tuition_amtb, student_status.uniform_amtb, student_status.books_amtb, student_status.total_amtb,
                student_status.discount_type, student_status.discount_percent, student_status.final_amtb, student_status.semester)
        cursor.execute(financial_status_query, values)
        financial_status_query = "SELECT * FROM financial_status WHERE ticket_id = %s"
        cursor.execute(financial_status_query, (get_ticketID['ticket_id'],))
        status_id_discounted = cursor.fetchone()
        if discounts:
            discount_insert_query = """INSERT INTO discounted_fees (status_id, tuition_discounted, books_discounted, uniform_discounted, total_discounted)
            VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(discount_insert_query, (status_id_discounted['status_id'], discounts.tuition_discounted, discounts.book_discounted, discounts.uniform_discounted, discounts.total_discounted))
            print(f"\n=== [FINANCIAL RECORD SETTED FOR STUDENT: {get_ticketID['first_name']}] ===")
            print(f"Original Amount: Php {float(student_status.total_amtb)} || Discount Applied: {float(student_status.discount_percent)}% || Final Amount: Php {float(student_status.final_amtb)}")
        else:
            print(f"\n=== [FINANCIAL RECORD SETTED FOR STUDENT: {get_ticketID['first_name']}] ===")
            print(f"Original Amount: Php {float(student_status.total_amtb)} || Discount Applied: {float(student_status.discount_percent)}% || Final Amount: Php {float(student_status.final_amtb)}")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print("\n[SETTING FAILED]", e)
    finally:
        my_sql.close()

def get_discount_rate(discount_type):
    if "academic excellence - full" in discount_type.lower():
        return 100
    elif "academic excellence - partial" in discount_type.lower():
        return 50
    elif "cultural" in discount_type.lower():
        return 70
    elif "athletic" in discount_type.lower():
        return 50
    elif "brassband" in discount_type.lower():
        return 100
    elif "freshmen" in discount_type.lower():
        return 15
    elif "alumni - grade 7 to 12" in discount_type.lower():
        return 40
    elif "alumni - grade 8 to 12" in discount_type.lower():
        return 35
    elif "alumni - grade 9 to 12" in discount_type.lower():
        return 30
    elif "alumni - grade 10 to 12" in discount_type.lower():
        return 25
    elif "alumni - grade 11 to 12" in discount_type.lower():
        return 20
    elif "sibling" in discount_type.lower():
        return 10
    elif "employee - child" in discount_type.lower():
        return 50
    elif "employee - sibling" in discount_type.lower():
        return 25
    elif "full - payment" in discount_type.lower():
        return 5
    elif "student - assistant" in discount_type.lower():
        return 0
    elif "none" in discount_type.lower():
        return 0


if __name__ == "__main__":
    main()