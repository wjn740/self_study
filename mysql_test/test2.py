#!/usr/bin/env python3

import mysql.connector

from mysql.connector import errorcode

from itertools import product

import urllib.request

from urllib.error import HTTPError

import io

import os

import re

from configparser import ConfigParser
from configparser import RawConfigParser
import configparser


########MAIN##############################################################

config = {
        'user' : 'qadb',
        'password' : '',
        'host' : '147.2.207.30',
        'database' : 'qadb',
        'raise_on_warnings': True,
        }
compare_products_list = list()

def read_database_init_data_pool():
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor()
        query = ("SELECT distinct `kernel_version`, `product`, `release` from performance_view")
        cursor.execute(query)
        i=0
        table=list()
        for (kernel_version, product, release) in cursor:
            table.append([kernel_version, product, release])
            print(i, table[i])
            i+=1
        compare_product_index_list=input("Please give your want products(eg. 1,3):").split(",")
        print(compare_product_index_list)
        for index in compare_product_index_list:
            compare_products_list.append(table[int(index)])
        print(compare_products_list)


            #print("submission_id={}, arch={}, product={}, release={}, host={}, log_url={}, testsuite={}, testcase={}, kernel_version={}".format(submission_id, arch, product, release, host, log_url, testsuite, testcase, kernel_version))


#Don't do create object at here.
            #TestCase(submission_id, arch, product, release, host, log_url, testsuite, test_time, testcase, kernel_version)

        cnx.close()

read_database_init_data_pool()
