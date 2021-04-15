#!/usr/bin/env python3.8

import os
import sys
import psycopg2
from flask import Flask, render_template, url_for, redirect, abort
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socket = SocketIO(app)

def random_location():
    global cur
    sql = "SELECT location_name FROM locations ORDER BY RANDOM() LIMIT 1;"
    cur.execute(sql)
    location = cur.fetchone()
    while location is not None:
        venue= ("\nThis week's location is: "+"".join(location))
        location = cur.fetchone()
        return venue

def delete_location():
    delete_id = input('Enter a location ID to delete:')
    print('Do you wish to proceed with deleting this record?')
    cur = conn.cursor()
    sql= "DELETE FROM locations WHERE location_id = (%s);"
    cur.execute(sql,(delete_id,))
    rows_deleted = cur.rowcount
    conn.commit()
    cur.close()


def insert_location():
    location_name =input('Enter a location:').upper()
    sql = """INSERT INTO locations(location_name) VALUES(%s) RETURNING location_id;"""
    cur = conn.cursor()
    cur.execute(sql, (location_name,))
    location_id = cur.fetchone()[0]
    conn.commit
    print('Successfully added '+str(location_name)+ ' to the CACC DB')
    print((location_id))

def print_locations():
    cur = conn.cursor()
    cur.execute("""SELECT * FROM locations;""")
    list = cur.fetchall()

    while list is not None:
        return(list)
        list = cur.fetchall()
        print (list)
    cur.close()


@app.route('/')
def serve_some_shit():
    return render_template('index.html')

@socket.on("keyword")
def serve_venue():
    venue = random_location()
    socket.emit("venue", {"location" : venue})

@socket.on("list_keyword")
def list_venue():
    list = print_locations()
    socket.emit("db_list", {"list" : list})

def init_program():
    global cur, conn
    conn = psycopg2.connect("dbname=cacc user=postgres")
    cur = conn.cursor()

if __name__ == '__main__':
    init_program()
    socket.run(app)
