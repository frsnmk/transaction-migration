from .connection import Koperasi

class Supplier:

    def fetch_all_name(self) ->list[str]:
        conn = Koperasi.create_connection()
        cur = conn.cursor(dictionary=True)
        sql = '''SELECT * FROM suppliers'''
        cur.execute(sql)
        res = [row['name'] for row in cur.fetchall()]
        return res