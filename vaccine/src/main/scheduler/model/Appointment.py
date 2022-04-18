import sys
sys.path.append("../util/*")
sys.path.append("../db/*")
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import random

class Appointment:
    def __init__(self, user):
        self.user = user

    def get(self, stauts):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)

        if stauts == 'patient':
            show_appointmnet = "SELECT AppointmentID, PUser, Username, App_time, VName FROM Appointments WHERE PUser = %s"
        else:
            show_appointmnet = "SELECT AppointmentID, PUser, Username , App_time, VName FROM Appointments WHERE Username = %s"

        try:
            cursor.execute(show_appointmnet, self.user)
            return cursor.fetchall()
        except pymssql.Error:
            print("Error occurred while running Appointments database")
            cm.close_connection()
        cm.close_connection()
        return None

    def get_appointmentID(self):
        return self.appoint

    def save_to_db(self, appointmentID, date, caregiver, patient, vaccine):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_appointment = "INSERT INTO Appointments VALUES (%s, %s, %s, %s, %s)"

        try:
            cursor.execute(add_appointment, (appointmentID, date, caregiver, patient, vaccine))
            conn.commit()
        except pymssql.Error:
            print("Error occurred when creating an appointment")
            cm.close_connection()
        print(" *** Reservation made successfully *** ")

        cm.close_connection()

    def cancel(self, appointmentID):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()
        check = conn.cursor()

        check_exist = "SELECT * FROM Appointments WHERE AppointmentID = %s"
        cancel_appointment = "DELETE FROM Appointments WHERE AppointmentID = %s"

        try:
            check.execute(check_exist, appointmentID)
            if check.fetchall():
                cursor.execute(cancel_appointment, appointmentID)
                print("Appointment cancelled")
                conn.commit()
            else:
                print("Please check your appoinment ID again.")
        except pymssql.Error:
            print("Error occurred when running Appointments database")
            cm.close_connection()

        cm.close_connection()
