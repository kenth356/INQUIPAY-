from connection import connectDB
from generator import generate_reference_no_CASHIN, generate_reference_no_SENDPAYMENT, generate_reference_no_SCHOOLREQS, generate_cashIN_date, generate_sendpayment_date, generate_schoolREQS_date
import adminCODE

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
        self.total_amtb = 0.0
        self.payment_status = ""
        self.discount_type = ""
        self.discount_percent = 0.0
        self.final_amt = 0.0
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
        self.purpose = ""

class notifications:
    def __init__(self):
        self.notif_id = 0
        self.notif_type = ""
        self.notif_message = ""
        self.notif_date = ""

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
    code = 2706
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

def manageTUI():
    student_status = financial_status()
    print("\n[MANAGE TUITION FEE PAYMENTS AND INQUIRIES]")
    student_id = int(input("Enter Student ID: "))
    student_status.tuition_amtb = float(input("Enter Tuition Fee Amount: "))
    student_status.uniform_amtb = float(input("Enter Uniform Amount: "))
    student_status.books_amtb = float(input("Enter Books Amount: "))
    student_status.discount_type = input("Enter discount type: ")
    student_status.semester = input("Enter semester: ")
    saveTUISTAT(student_id, student_status)

def manageINQ():
    while True:
        print("\n[MANAGE INQUIRIES]")
        print("1. Toggle tuition notifications")
        print("2. Toggle uniform notifications")
        print("3. Toggle books notifcations")
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
        student_schoolREQ_status_query = "SELECT tuition_amtb FROM financial_status WHERE ticket_id = %s"
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

def saveTUISTAT(student_id, student_status):
    my_sql = connectDB()
    cursor = my_sql.cursor(dictionary=True)
    student_status.discount_percent = get_discount_rate(student_status.discount_type)
    student_status.total_amtb = student_status.tuition_amtb + student_status.uniform_amtb + student_status.books_amtb
    student_status.final_amtb = student_status.total_amtb - (student_status.total_amtb * student_status.discount_percent / 100)
    try:
        get_ticketID_query = "SELECT * FROM student WHERE student_id = %s"
        cursor.execute(get_ticketID_query, (student_id,))
        get_ticketID = cursor.fetchone()
        financial_status_query = """INSERT INTO financial_status (ticket_id, tuition_amtb, uniform_amtb, books_amtb,
        discount_type, discount_percent, final_amtb, semester)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (get_ticketID['ticket_id'], student_status.tuition_amtb, student_status.uniform_amtb, student_status.books_amtb,
                student_status.discount_type, student_status.discount_percent, student_status.final_amtb, student_status.semester)
        cursor.execute(financial_status_query, values)
        print(f"\n=== [FINANCIAL RECORD SETTED FOR STUDENT: {get_ticketID['first_name']}] ===")
        print(f"Original Amount: Php {float(student_status.total_amtb)} || Discount Applied: {float(student_status.discount_percent)}% || Final Amount: Php {float(student_status.final_amtb)}")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print("\n[SETTING FAILED]", e)
    finally:
        my_sql.close()

def get_discount_rate(discount_type):
    if discount_type.lower() in ("academic excellence full"):
        return 100
    elif discount_type.lower() in ("academic excellence partial"):
        return 50
    elif discount_type.lower() in "cultural":
        return 70
    elif discount_type.lower() in "athletic":
        return 50
    elif discount_type.lower() in "brassband":
        return 100
    elif discount_type.lower() in "freshmen":
        return 15
    elif discount_type.lower() in "alumni grade 7 to 12":
        return 40
    elif discount_type.lower() in "alumni grade 8 to 12":
        return 35
    elif discount_type.lower() in "alumni grade 9 to 12":
        return 30
    elif discount_type.lower() in "alumni grade 10 to 12":
        return 25
    elif discount_type.lower() in "alumni grade 11 to 12":
        return 20
    elif discount_type.lower() in "sibling":
        return 10
    elif discount_type.lower() in "employee child":
        return 50
    elif discount_type.lower() in "employee sibling":
        return 25
    elif discount_type.lower() in "full payment":
        return 5
    elif discount_type.lower() in "student assistant":
        return 0
    else:
        return 0

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
        student_query = "SELECT * FROM student WHERE first_name = %s"
        cursor.execute(student_query, (REGISTERED_name,))
        student_data = cursor.fetchone()
        if student_data is None:
            print("\nSTUDENT NOT FOUND")
            return
        notification_query = "SELECT * FROM notifications WHERE student_id = %s ORDER BY notif_date DESC"
        cursor.execute(notification_query, (student_data['student_id'],))
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
    check_balance_query = "SELECT * FROM student WHERE first_name = %s"
    cursor.execute(check_balance_query, (REGISTERED_name,))
    student_data = cursor.fetchone()
    if student_data is None:
        print("\n[STUDENT DATA DOES NOT EXISTS]")
    print(f"\n=== [YOUR CURRENT BALANCE: {student_data['balance']}]")

def helpCENTER():
    print()

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
        sender_query = "SELECT * FROM student WHERE first_name = %s"
        cursor.execute(sender_query, (REGISTERED_name,))
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
        insert_transaction = """INSERT INTO payment_transaction (ticket_id, sender_name, receiver_name, payment_amount, reference_no)
        VALUES (%s, %s, %s, %s, %s)"""
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

def savePAY_TO_SCHOOLREQ_PROCESS(transactions):
    transactions.payment_date = generate_schoolREQS_date()
    transactions.reference_no = generate_reference_no_SCHOOLREQS()
    my_sql = connectDB()
    cursor = my_sql.cursor(dictionary=True)
    try:
        student_query = "SELECT * FROM student WHERE first_name = %s"
        cursor.execute(student_query, (REGISTERED_name,))
        student = cursor.fetchone()
        if student is None:
            print("\n[USER DOES NOT EXIST]")
            return
        if student['balance'] < transactions.payment_amount:
            print("\n[INSUFFICIENT FUNDS]")
            return
        schoolREQ_query = "SELECT * FROM financial_status WHERE ticket_id = %s"
        cursor.execute(schoolREQ_query, (student['ticket_id'],))
        schoolREQ_data = cursor.fetchone()
        if schoolREQ_data is None:
            print("\n[NO RECORD FOUND]")
            return
        student_transaction_query = "UPDATE student SET balance = balance - %s WHERE student_id = %s"
        cursor.execute(student_transaction_query, (transactions.payment_amount, student['student_id']))
        if transactions.purpose.lower() in "tuition":
            status_column = "tuition_status"
            amount_due = float(schoolREQ_data['tuition_amtb'])
        elif transactions.purpose.lower() in "books":
            status_column = "books_status"
            amount_due = float(schoolREQ_data['books_amtb'])
        elif transactions.purpose.lower() in "uniform":
            status_column = "uniform_status"
            amount_due = float(schoolREQ_data['uniform_amtb'])
        if transactions.payment_amount >= amount_due:
            new_status = "APPROVED"
        else:
            new_status = "SEMI-APPROVED"
        update_financial_stat_query = f"UPDATE financial_status SET {status_column} = %s, payment_status = %s WHERE status_id = %s"
        cursor.execute(update_financial_stat_query, (new_status, "SEMI-PAID" if new_status == "SEMI-APPROVED" else "PAID", schoolREQ_data['status_id']))
        insert_payment_query = """INSERT INTO payment_transaction (ticket_id, status_id, payment_amount, reference_no,
        sender_name, receiver_name) VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_payment_query, (student['ticket_id'], schoolREQ_data['status_id'], transactions.payment_amount, transactions.reference_no, student['first_name'], "DYCI Elida Finance"))
        print("\n=== [PAYMENT SUCCESSFUL] ===")
        print(f"REFERENCE NO.: {transactions.reference_no}")
        print(f"PURPOSE OF PAYMENT: {transactions.purpose}")
        print(f"AMOUNT PAID: Php {transactions.payment_amount}")
        print(f"STATUS: {new_status}")
        print(f"[YOUR CURRENT BALANCE: {student['balance']}]")
        print(f"=== DATE: {transactions.payment_date} ===")
        my_sql.commit()
    except Exception as e:
        my_sql.rollback()
        print("\n[PAYMENT FAILED]", e)
    finally:
        my_sql.close()


if __name__ == "__main__":
    main()