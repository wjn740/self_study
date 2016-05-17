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




TestCase_gloale_list = set()

def search_list(objects_list, func):
    for x in objects_list:
        if func(x):
            return True
    return False

def select_where_string(k, tc, ts, h, r, p, a):
    where_string=str("")
    start = True
    if k:
        where_string="".join([where_string, " `kernel_version` = \'"+k+"\' "])
        start = False
    print(where_string)
    if tc:
        if start == False:
            where_string="".join([where_string, "and"])
        where_string="".join([where_string, " `testcase` = '"+tc+"' "])
        start = False
    print(where_string)

    if ts:
        if start == False:
            where_string="".join([where_string, "and"])
        where_string="".join([where_string, " `testsuite` = '"+ts+"' "])
        start = False
    print(where_string)

    if h:
        if start == False:
            where_string="".join([where_string, "and"])
        where_string="".join([where_string, " `host` = '"+h+"' "])
        start = False
    print(where_string)

    if r:
        if start == False:
            where_string="".join([where_string, "and"])
        where_string="".join([where_string, " `release` = '"+r+"' "])
        start = False
    print(where_string)
    if p:
        if start == False:
            where_string="".join([where_string, "and"])
        where_string="".join([where_string, " `product` = '"+p+"' "])
        start = False
    print(where_string)
    if a:
        if start == False:
            where_string="".join([where_string, "and"])
        where_string="".join([where_string, " `arch` = '"+a+"' "])
    print(where_string)
    return where_string



def read_data_perf_view_with_where(where_string):
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

        select_string="".join(["SELECT * from performance_view", " where ", where_string, ";"])
        #select_string="SELECT * from performance_view where  `kernel_version` = '3.12.57' and `testsuite` = 'qa_iozone_doublemem_ext3' and `host` = 'apac2-ph033.bej.suse.com' and `release` = 'GM' and `product` = 'SLES-12-SP1' and `arch` = 'x86_64' ;"

        print(select_string)
        query = (select_string)
        cursor.execute(query)
        testcase_list=set()
        for (submission_id, arch, product, release, host, log_url, testsuite, test_time, testcase, kernel_version) in cursor:
            #print(submission_id, arch, product, release, host, testsuite, test_time, testcase, kernel_version)
            testcase_list.add(TestCase(submission_id, arch, product, release, host, log_url, testsuite, test_time, testcase, kernel_version))


        search_list(testcase_list, lambda x: print(x.testsuite, x.testcase, x.host, x.kernel_long_version, x.product, x.release))
        cnx.close()
#================================DATABASE==============================================================================================
class TestCase():
    def __init__(self, submission_id="", arch="", product="", release="", host="", log_url="", testsuite="", test_time="", testcase="", kernel_version=""):
        self.submission_id=submission_id
        self.arch = arch
        self.product = product
        self.release = release
        self.host = host
        self.log_url = log_url
        self.testsuite = testsuite
        self.test_time = test_time
        self.testcase = testcase
        self.kernel_version = kernel_version
        self.kernel_long_version = self.read_kernel_long_version()

    def __repr__(self):
        return self.testcase

    def read_testcase(self):
        f = urllib.request.urlopen(self.log_url+"/"+self.testcase)
        for line in f:
            print(line)

    def read_kernel_long_version(self):
        with urllib.request.urlopen(self.log_url+"/"+'kernel') as response:
            for line in response:
                line = line.decode('utf-8')
                patten=re.compile(r'(Name) *: .*(kernel)-(default)*')
                match1 = patten.match(line)
                if match1:
                    flavor=match1.group(3)
                    continue
                patten=re.compile(r'(Version) *: (.*)')
                match1 = patten.match(line)
                if match1:
                    major=match1.group(2)
                    continue
                patten=re.compile(r'(Release) *: ([0-9][0-9]*)\.([0-9]*)\.*([0-9].*)*')
                match1 = patten.match(line)
                if match1:
                    if match1.group(4):
                        minor='.'.join([match1.group(2), match1.group(3)])
                        continue
                    else:
                        minor='.'.join([match1.group(2)])
                        continue
                if flavor and major and minor:
                    break
            return "-".join([major, minor, flavor ])



########MAIN##############################################################

config = {
        'user' : 'qadb',
        'password' : '',
        'host' : '147.2.207.30',
        'database' : 'qadb',
        'raise_on_warnings': True,
        }

product_set = set()
machine_set = set()
arch_set = set()
release_set = set()
host_set = set()
testsuite_set = set()
kernel_version_set = set()
testcase_set = set()

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

#    query = ("SELECT distinct host from performance_view")
#    cursor.execute(query)
#    for h in cursor:
#        machine_set.add(h[0])
#    print(machine_set)
#
#    query = ("SELECT distinct product from performance_view")
#    cursor.execute(query)
#    for h in cursor:
#        product_set.add(h[0])
#    print(product_set)
#
#    query = ("SELECT distinct arch from performance_view")
#    cursor.execute(query)
#    for h in cursor:
#        arch_set.add(h[0])
#    print(arch_set)
#
#    query = ("SELECT distinct `release` from performance_view")
#    cursor.execute(query)
#    for h in cursor:
#        release_set.add(h[0])
#    print(release_set)
#
#
#    query = ("SELECT distinct `host` from performance_view")
#    cursor.execute(query)
#    for h in cursor:
#        host_set.add(h[0])
#    print(host_set)
#
#    query = ("SELECT distinct `testsuite` from performance_view")
#    cursor.execute(query)
#    for h in cursor:
#        testsuite_set.add(h[0])
#    print("testcase=",testsuite_set)
#
#    query = ("SELECT distinct `testcase` from performance_view")
#    cursor.execute(query)
#    for h in cursor:
#        testcase_set.add(h[0])
#    print("testcaes=",testcase_set)
#
#    query = ("SELECT distinct `kernel_version` from performance_view")
#    cursor.execute(query)
#    for h in cursor:
#        kernel_version_set.add(h[0])
#    print(kernel_version_set)

        query = ("SELECT * from performance_view")
        cursor.execute(query)
        for (submission_id, arch, product, release, host, log_url, testsuite, test_time, testcase, kernel_version) in cursor:
            arch_set.add(arch)
            product_set.add(product)
            release_set.add(release)
            host_set.add(host)
            testsuite_set.add(testsuite)
            testcase_set.add(testcase)
            kernel_version_set.add(kernel_version)
            #print("submission_id={}, arch={}, product={}, release={}, host={}, log_url={}, testsuite={}, testcase={}, kernel_version={}".format(submission_id, arch, product, release, host, log_url, testsuite, testcase, kernel_version))

#Don't do create object at here.
            #TestCase(submission_id, arch, product, release, host, log_url, testsuite, test_time, testcase, kernel_version)

        cnx.close()

read_database_init_data_pool()
print(kernel_version_set)
kernel_input = input("[kernel]:")
print(testcase_set)
testcase_input = input("[testcase]:")
print(testsuite_set)
testsuite_input = input("[testsuite]:")
print(host_set)
host_input = input("[host]:")
if not kernel_input:
    print(release_set)
    release_input = input("[release]:")
    print(product_set)
    product_input = input("[product]:")
print(arch_set)
arch_input = input("[arch]:")
kernel_compare_list = kernel_input.split(",")
testcase_compare_list = testcase_input.split(",")
testsuite_compare_list = testsuite_input.split(",")
host_compare_list = host_input.split(",")
if not kernel_input:
    release_compare_list = release_input.split(",")
    product_compare_list = product_input.split(",")
else:
    release_compare_list = [""]
    product_compare_list = [""]
arch_compare_list = arch_input.split(",")



#print(kernel_compare_list)
#print(testcase_compare_list)
#print(testsuite_compare_list)
#print(host_compare_list)
#print(release_compare_list)
#print(product_compare_list)
#print(arch_compare_list)


#print("Hello,world!")
for k,tc,ts,h,r,p,a in product(kernel_compare_list, testcase_compare_list, testsuite_compare_list, host_compare_list, release_compare_list, product_compare_list, arch_compare_list):
    #print("Hello,world!")
    #print(k, tc, ts, h, r, p, a)
    if k or tc or ts or h or r or p or a:
        where_string=select_where_string(k, tc, ts, h, r, p, a)
        read_data_perf_view_with_where(where_string)


    #for testcase in TestCase_gloale_list:
    #    if k == testcase.kernel_version and tc == testcase.testcase and ts == testcase.testsuite and h == testcase.host and r == testcase.release and p == testcase.product and a == testcase.arch:
    #        print(k, tc, ts, h, r, p, a)
    #        testcase.read_testcase()

#print("Global testcase list:\n", TestCase_gloale_list)

#host_input = input("[host]:")

#print(search_list(TestCase_gloale_list, lambda x: x.host == host_input))
