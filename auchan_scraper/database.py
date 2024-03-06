import os
import sqlite3


def create_table():
    current_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(os.path.join(current_path, "auchan.db"))
    curr = conn.cursor()
    curr.execute("""DROP TABLE IF EXISTS auchan""")
    curr.execute(
        """CREATE TABLE auchan(
        product_name text,
        category_name text,
        price text,
        volume text
    )"""
    )
    conn.commit()
    conn.close()


create_table()
create_table()
