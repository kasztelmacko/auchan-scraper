import sqlite3

def create_table():
    conn = sqlite3.connect('auchan.db')
    curr = conn.cursor()
    curr.execute("""DROP TABLE IF EXISTS auchan""")
    curr.execute("""CREATE TABLE auchan(
        product_name text,
        category_name text,
        price text,
        volume text
    )""")
    conn.commit()
    conn.close()

create_table()