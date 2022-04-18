import sys
from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from model.Appointment import Appointment
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime
import random


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    if len(tokens) != 3:
        print("Re-enter the information please!")
        return

    p_user = tokens[1]
    p_pass = tokens[2]

    if username_exists_patient(p_user):
        print("Patient username already taken.")
        return
    
    salt = Util.generate_salt()
    hash = Util.generate_hash(p_pass, salt)

    try:
        patient = Patient(p_user, salt=salt, hash=hash)
        patient.save_to_db()
        print(" *** Account created successfully *** ")
    except pymssql.Error:
        print("Create failed. Please try again.")
        return


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    try:
        caregiver = Caregiver(username, salt=salt, hash=hash)
        # save to caregiver information to our database
        try:
            caregiver.save_to_db()
        except:
            print("Create failed, Cannot save")
            return
        print(" *** Account created successfully *** ")
    except pymssql.Error:
        print("Create failed")
        return


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error:
        print("Error occurred when checking username")
        cm.close_connection()
    cm.close_connection()
    return False


def username_exists_patient(p_user):
    p_cm = ConnectionManager()
    p_conn = p_cm.create_connection()

    select_p_user = "SELECT * FROM Patients WHERE PUser = %s"
    try:
        p_cursor = p_conn.cursor(as_dict=True)
        p_cursor.execute(select_p_user, p_user)
        for row in p_cursor:
            return row['PUser'] is None
    except pymssql.Error:
        print("Error occurred when checking Patient's username")
        p_cm.close_connection()
    p_cm.close_connection()
    return False


def login_patient(tokens):
    global current_patient
    if current_patient is not None or current_caregiver is not None:
        print("You're already logged-in.")
        return

    if len(tokens) != 3:
        print("Information missing. Please try again")
        return

    p_user = tokens[1]
    p_pass = tokens[2]

    patient = None
    try:
        patient = Patient(p_user, password=p_pass).get()
    except pymssql.Error:
        print("Error occurred when logging in")

    # check if the login was successful
    if patient is None:
        print("Patient username incorrect or invalid")
    else:
        print("Patient logged in as: " + p_user)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("Already logged-in!")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        try:
            caregiver = Caregiver(username, password=password).get()
        except:
            print("Get Failed")
            return
    except pymssql.Error:
        print("Error occurred when logging in")

    # check if the login was successful
    if caregiver is None:
        print("Please try again!")
    else:
        print("Caregiver logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    if len(tokens) != 2:
        print("Enter the date to search for.")
        return

    cm = ConnectionManager()
    conn = cm.create_connection()

    search_date = tokens[1]

    if validate_date(search_date):
        return

    search = "SELECT Username FROM Availabilities WHERE Time = %s"
    vacc = "SELECT * FROM Vaccines"

    try:
        cursor = conn.cursor(as_dict=True)

        cursor.execute(search, search_date)
        avail_result = cursor.fetchall()

        cursor.execute(vacc)
        vacc_result = cursor.fetchall()

        print("Available Caregivers: ")
        for row_a in avail_result:
            print("• " + row_a['Username'].capitalize())

        print("\nAvailable Vaccines: ")
        for row_v in vacc_result:
            print("- " + row_v['VName'].capitalize() + ": " + str(row_v['Doses']))
    except pymssql.Error:
        print("Error occurred when searching for available caregivers")
        cm.close_connection()
    cm.close_connection()


def validate_date(token):
    try:
        datetime.datetime.strptime(token, '%m-%d-%Y')
    except ValueError:
        print("Incorrect date/date format. Please enter valid date iin MM-DD-YYYY format")
        return True
    return False


def reserve(tokens):
    global current_patient

    if current_patient is None:
        print("Please log in as a patient first")
        return

    patient = current_patient.get_p_user()

    if len(tokens) != 3:
        print("Please enter the date and vaccine you wish to receive")
        return

    date = tokens[1]
    vacc = tokens[2].lower()
    
    if validate_date(date):
        return

    cm = ConnectionManager()
    conn = cm.create_connection()

    #Genrate Unique Appointment ID
    appointmentID = random.randint(1000000, 9999999)
    while app_id_exists(appointmentID):
        appointmentID = random.randint(1000000, 9999999)

    try:
        #Random Caregiver
        search_care = "SELECT Username FROM Availabilities WHERE Time = %s "
        care_cursor = conn.cursor()
        care_cursor.execute(search_care, date)

        avail_list = care_cursor.fetchall()
        if len(avail_list) == 0:
            print("No caregivers available on the specified date.")
            cm.close_connection()
            return

        rand_num = random.randint(0, len(avail_list) - 1)
        rand_caregiver = avail_list[rand_num][0]

        #Check Vaccine
        try:
            vacc_cursor = conn.cursor()
            search_vacc = "SELECT * FROM Vaccines WHERE VName = %s"
            vacc_cursor.execute(search_vacc, vacc)

            if not vacc_cursor.fetchall():
                vacc_cursor.execute("SELECT DISTINCT VName FROM Vaccines")
                vacc_list = vacc_cursor.fetchall()

                print("Please select from the available vaccines below: ")
                for row in vacc_list:
                    print(row[0].capitalize())
                return

        except pymssql.Error:
            print("Error occured while checking for vaccines.")
            cm.close_connection()
            return
        
        #Make Reservation
        appointment = Appointment(patient)
        
        try:
            appointment.save_to_db(appointmentID, date, rand_caregiver, patient, vacc)
        except pymssql.Error:
            print("Error occurred when creating an appointment")
            cm.close_connection()
        print("Your Caregiver: " + rand_caregiver.capitalize() + "\nYour Appointment ID: " + str(appointmentID))
    except pymssql.Error:
        print("Create failed")
        cm.close_connection()
        return
    cm.close_connection()


def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]

    if validate_date(date):
        return

    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        try:
            current_caregiver.upload_availability(d)
        except:
            print("Upload Availability Failed")
        print("Availability uploaded!")
    except ValueError:
        print("Please enter a valid date! in a format of MM-DD-YYYY")
    except pymssql.Error as db_err:
        print("Error occurred when uploading availability")

def app_id_exists(app_id):
        cm = ConnectionManager()
        conn = cm.create_connection()

        search_id = "SELECT AppointmentID FROM Appointments WHERE AppointmentID = %s"

        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute(search_id, app_id)
            for row in cursor:
                return row['AppointmentID'] is not None
        except pymssql.Error:
            print("Error occurred while checking for appointment ID")
            cm.close_connection()
        cm.close_connection()
        return False

def cancel(tokens):
    global current_caregiver
    global current_patient

    if len(tokens) != 2:
        print("Please input the appointment ID only.")
        return

    if current_patient is not None:
        appointment = Appointment(current_patient.get_p_user())
    elif current_caregiver is not None:
        appointment = Appointment(current_caregiver.get_username())
    else:
        print("Please login first.")

    appointment.cancel(tokens[1])


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        try:
            vaccine = Vaccine(vaccine_name, doses).get()
        except:
            print("Failed to get Vaccine!")
            return
    except pymssql.Error:
        print("Error occurred when adding doses")

    # check 3: if getter returns null, it means that we need to create the vaccine and insert it into the Vaccines
    #          table

    if vaccine is None:
        try:
            vaccine = Vaccine(vaccine_name, doses)
            try:
                vaccine.save_to_db()
            except:
                print("Failed To Save")
                return
        except pymssql.Error:
            print("Error occurred when adding doses")
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            try:
                vaccine.increase_available_doses(doses)
            except:
                print("Failed to increase available doses!")
                return
        except pymssql.Error:
            print("Error occurred when adding doses")

    print("Doses updated!")


def show_appointments(tokens):
    global current_caregiver
    global current_patient

    if current_patient is not None or current_caregiver is not None:
        if current_patient is not None:
            user = Appointment(current_patient.get_p_user()).get('patient')
            username = 'PUser'
            assigned = 'Username'
        else:
            user = Appointment(current_caregiver.get_username()).get('caregiver')
            username = 'Username'
            assigned = 'PUser'

        if user:
            print("Hello " + user[0][username] + ". You have " + str(len(user)) + " appointment(s). ")
            print("Here is/are your appointment(s) information: \n")
            for row in user:
                print("Your appointment ID: " + str(row['AppointmentID']))
                print("Appointed vaccine: " + row['VName'].capitalize())
                print("Appointment date: " + str(row['App_time']))
                print("You're assgined to: " + row[assigned] + "\n")
        else:
            print("No reservations made/available.")

    else:
        print("You must be logged in to view your appointment. Please login first.")
        return


def logout(tokens):
    global current_caregiver
    global current_patient

    if len(tokens) != 1:
        print("Invalid command. Please check your command again")
        return

    if current_caregiver is not None or current_patient is not None:
        if current_caregiver is not None:
            current_caregiver = None
        else:
            current_patient = None
        print("You have succesfully logged out")
    else:
        print("You are not logged in")


def start():
    stop = False
    while not stop:
        print()
        print(" *** Please enter one of the following commands *** ")
        print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
        print("> create_caregiver <username> <password>")
        print("> login_patient <username> <password>")  #// TODO: implement login_patient (Part 1)
        print("> login_caregiver <username> <password>")
        print("> search_caregiver_schedule <date>")  #// TODO: implement search_caregiver_schedule (Part 2)
        print("> reserve <date> <vaccine>") #// TODO: implement reserve (Part 2)
        print("> upload_availability <date>")
        print("> cancel <appointment_id>") #// TODO: implement cancel (extra credit)
        print("> add_doses <vaccine> <number>")
        print("> show_appointments")  #// TODO: implement show_appointments (Part 2)
        print("> logout") #// TODO: implement logout (Part 2)
        print("> Quit")
        print()
        response = ""
        print("> Enter: ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Type in a valid argument")
            break

        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Try Again")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == "cancel":
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Thank you for using the scheduler, Goodbye!")
            stop = True
        else:
            print("Invalid Argument")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
