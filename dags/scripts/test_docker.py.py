#!/usr/bin/env python
import pandas as pd
import requests
import json
import psycopg2
import psycopg2.extras as extras

'''
dataset = "https://gist.githubusercontent.com/mmphego/5b6fc4d6dc3c8fba4fce9d994a2fe16b/raw/ab5df0e76812e13df5b31e466a5fb787fac0599a/wine_quality.csv"
df = pd.read_csv(dataset)
df.head()
df.info()
'''

def create_table(conn):
    cur = conn.cursor()
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS  test(
        name VARCHAR(20));
        """)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    else:
        conn.commit()

def insert_values(conn):
    query = """INSERT INTO test(name) VALUES ('Anushaaaaaa');"""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()


def main():

    conn = psycopg2.connect(
        host="postgres",  # changed from 'localhost' so it would work with docker
        database="premji_test1",
        user="postgres",  # your postgres username
        password="YOU_PASSWORD")

    print("Transforming...")
    create_table(conn)
    print("Loading...")
    insert_values(conn)
    print("Finished.")


if __name__ == "__main__":
    main()

