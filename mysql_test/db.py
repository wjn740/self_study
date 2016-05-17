#!/usr/bin/env python3

import mysql.connector

cnx = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='')

cnx.close()
