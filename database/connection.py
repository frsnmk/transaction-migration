import mysql.connector

class Koperasi:
    @staticmethod
    def create_connection():
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="management_koperasi",
            
        )
        return mydb