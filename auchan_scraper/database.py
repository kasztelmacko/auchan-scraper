import os
import sqlite3


def create_table():
    current_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(os.path.join(current_path, "auchan.db"))
    curr = conn.cursor()
    curr.execute("""DROP TABLE IF EXISTS auchan""")
    curr.execute(
        """CREATE TABLE auchan(
        product_id integer PRIMARY KEY AUTOINCREMENT,
        product_name text,
        category_name text,
        price integer,
        currency text,
        volume integer,
        unit text,
        volume_info text,
        package_unit text,
        package_size integer)
    """
    )

    curr.execute("""DROP TABLE IF EXISTS category""")
    curr.execute(
        """CREATE TABLE category(
        id integer,
        url text,
        cat_1 text,
        cat_2 text,
        product_name text
    )"""
    )
    conn.commit()
    conn.close()


create_table()
