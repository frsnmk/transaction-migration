from .connection import Koperasi

class Employee:
    def fetch_all():
        conn = Koperasi.create_connection()
        cur = conn.cursor(dictionary=True)
        sql = '''SELECT * FROM employees'''
        cur.execute(sql)
        res = cur.fetchall()
        return res
    
    def fetch_all_name(self):
        conn = Koperasi.create_connection()
        cur = conn.cursor(dictionary=True)
        sql = '''SELECT * FROM employees'''
        cur.execute(sql)
        res = [row['name'] for row in cur.fetchall()]
        return res
    