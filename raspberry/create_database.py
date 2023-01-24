#!/usr/bin/env python3

import sqlite3
import time
import os


def create_database():
    if os.path.exists("card_logs.db"):
        os.remove("card_logs.db")
        print("An old database removed.")
    connection = sqlite3.connect("card_logs.db")
    cursor = connection.cursor()
    cursor.execute(""" CREATE TABLE card_logs (
        log_id number,
        card_uid text,
        date text,
        reader text
    )""")
    connection.commit()
    connection.close()
    print("The new database created.")


if __name__ == "__main__":
    create_database()
