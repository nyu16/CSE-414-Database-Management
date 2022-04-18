import sys
sys.path.append("../util/*")
sys.path.append("../db/*")
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql

class Patient:
    def __init__(self, p_user, password=None, salt=None, hash=None):
        self.p_user = p_user
        self.password = password
        self.salt = salt
        self.hash = hash

    def get(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)

        get_patient_details = "SELECT Salt, Hash FROM Patients WHERE PUser = %s"
        try:
            cursor.execute(get_patient_details, self.p_user)
            for row in cursor:
                curr_salt = row['Salt']
                curr_hash = row['Hash']
                calculated_hash = Util.generate_hash(self.password, curr_salt)
                if not curr_hash == calculated_hash:
                    cm.close_connection()
                    return None
                else:
                    self.salt = curr_salt
                    self.hash = calculated_hash
                    return self
        except pymssql.Error:
            print("Error occurred when getting Patients")
            cm.close_connection()

        cm.close_connection()
        return None

    def get_p_user(self):
        return self.p_user

    def get_salt(self):
        return self.salt

    def get_hash(self):
        return self.hash

    def save_to_db(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_patients = "INSERT INTO Patients VALUES (%s, %s, %s)"
        try:
            cursor.execute(add_patients, (self.p_user, self.salt, self.hash))
            conn.commit()
        except pymssql.Error as db_err:
            print("Error occurred when inserting Patient(s)")
            sqlrc = str(db_err.args[0])
            print("Exception code: " + str(sqlrc))
            cm.close_connection()
        cm.close_connection()
