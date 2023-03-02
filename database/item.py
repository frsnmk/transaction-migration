from .connection import Koperasi

class Item:
    def fetch_all(self):
        conn = Koperasi.create_connection()
        cur = conn.cursor(dictionary=True)
        sql = '''SELECT * FROM items'''
        cur.execute(sql)
        res = cur.fetchall()
        return res
    
    def get_barcode_by_item_name(self, item_name):
        conn = Koperasi.create_connection()
        cur = conn.cursor(dictionary=True)
        sql = f'''SELECT * FROM items WHERE name ={item_name}'''
        cur.execute(sql)
        res = cur.fetchone()
        return res