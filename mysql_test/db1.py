#!/usr/bin/env python3

import mysql.connector

from mysql.connector import errorcode

from itertools import product

import urllib.request

from urllib.error import HTTPError

import io

import os

import re

import sys

import getopt

from configparser import ConfigParser
from configparser import RawConfigParser
import configparser

#用于记录哪些产品参与对比
compare_products_list = list()

kernel_compare_list = list()
product_compare_list = list()
release_compare_list = list()

TestCase_gloale_list = list()

class benchmark():
    """flag mean that value is more bigger more better or more smaller more better."""
    def __init__(self, name, value, flag):
        self.name = name
        self.value = value
        self.flag = flag

    def __repr__(self):
        return ":".join([self.name, self.value])

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
        testcase_list=list()
        for (submission_id, arch, product, release, host, log_url, testsuite, test_time, testcase, kernel_version) in cursor:
            #print(submission_id, arch, product, release, host, testsuite, test_time, testcase, kernel_version)
            testcase_list.append(TestCase(submission_id, arch, product, release, host, log_url, testsuite, test_time, testcase, kernel_version))


        search_list(testcase_list, lambda x: print(x.testsuite, x.testcase, x.host, x.kernel_long_version, x.product, x.release, x.benchmark))
        cnx.close()
        return testcase_list
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
        self.testcase_benchmark()

    def __repr__(self):
        return "<"+self.testcase+">"

    def read_testcase(self):
        f = urllib.request.urlopen(self.log_url+"/"+self.testcase)
        for line in f:
            print(line)

    def testcase_benchmark(self):
        f = urllib.request.urlopen(self.log_url+"/"+self.testcase)
        if self.testcase == 'reaim-ioperf':
            self.benchmark_reaim_ioperf()
            return
        if self.testcase == 'sysbench-cpu':
            return
        if self.testcase == 'sysbench-threads':
            return
        if self.testcase == 'sysbench-memory':
            return
        if self.testcase == 'sysbench-mutex':
            return
        if self.testcase == 'sysbench-oltp':
            return
        if self.testcase == 'tiobench-doublemem-async':
            return
        if self.testcase == 'bonnie++-async':
            return
        if self.testcase == 'bonnie++-fsync':
            return
        if self.testcase == 'dbench4-async':
            return
        if self.testcase == 'dbench4-fsync':
            return
        if self.testcase == 'kernbench':
            return
        if self.testcase == 'libmicro-contextswitch':
            return
        if self.testcase == 'libmicro-file':
            return
        if self.testcase == 'libmicro-memory':
            return
        if self.testcase == 'libmicro-process':
            return
        if self.testcase == 'libmicro-regular':
            return
        if self.testcase == 'libmicro-socket':
            return
        if self.testcase == 'lmbench-bcopy':
            return
        if self.testcase == 'lmbench-ctx':
            return
        if self.testcase == 'lmbench-file':
            return
        if self.testcase == 'lmbench-local':
            return
        if self.testcase == 'lmbench-mem':
            return
        if self.testcase == 'lmbench-ops':
            return
        if self.testcase == 'lmbench-syscall':
            return
        if self.testcase == 'netperf-fiber-tcp':
            return
        if self.testcase == 'netperf-fiber-udp':
            return
        if self.testcase == 'netperf-fiber-tcp6':
            return
        if self.testcase == 'netperf-fiber-udp6':
            return
        if self.testcase == 'netperf-loop-tcp':
            return
        if self.testcase == 'netserver-start':
            return
        if self.testcase == 'netperf-loop-udp':
            return
        if self.testcase == 'pgbench-small-ro':
            return
        if self.testcase == 'pgbench-small-rw':
            return
        if self.testcase == 'iozone-doublemem-async':
            return
        if self.testcase == 'iozone-doublemem-fsync':
            return
        if self.testcase == 'qa_siege_performance':
            return


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


    def benchmark_reaim_ioperf(self):
        pattern=re.compile(b'Max Jobs per Minute ([0-9].*\.*[0-9]*)')
        self.benchmark = list()
        for line in urllib.request.urlopen(self.log_url+"/"+self.testcase):
            m = pattern.match(line)
            if m:
                value=str(m.group(1), 'utf-8')
                self.benchmark.append(benchmark('Jobs_per_Minute', value, 1))
                continue




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
            host_set.add(host)
            testsuite_set.add(testsuite)
            testcase_set.add(testcase)
            #print("submission_id={}, arch={}, product={}, release={}, host={}, log_url={}, testsuite={}, testcase={}, kernel_version={}".format(submission_id, arch, product, release, host, log_url, testsuite, testcase, kernel_version))

#Don't do create object at here.
            #TestCase(submission_id, arch, product, release, host, log_url, testsuite, test_time, testcase, kernel_version)

        query = ("SELECT distinct `kernel_version`, `product`, `release` from performance_view")
        cursor.execute(query)
        i=0
        table=list()
        for (kernel_version, product, release) in cursor:
            table.append([kernel_version, product, release])
            kernel_version_set.add(kernel_version)
            product_set.add(product)
            release_set.add(release)

            print(i, table[i])
            i+=1
        cnx.close()
        compare_product_index_list=input("Please give your want products(eg. 1,3):").split(",")
        print(compare_product_index_list)
        for index in compare_product_index_list:
            try:
                compare_products_list.append(table[int(index)])
                kernel_compare_list.append(table[int(index)][0])
                product_compare_list.append(table[int(index)][1])
                release_compare_list.append(table[int(index)][2])
            except IndexError:
                sys.stderr.write("choose error, total amount: "+str(len(table))+"\n"+"out of list!!\n")
                sys.exit(1)
        print(compare_products_list)

#---------------START-------------------------------
args = sys.argv[1:]

optlist, args = getopt.getopt(args,'k:p:r:s:t:h:a:',['kernel', 'product', 'release', 'testsuite', 'testcase', 'host', 'arch'])

for o,v in optlist:
    if o in ("-k", "--kernel"):
        kernel_compare_list = v.split(",")
    if o in ("-p", "--product"):
        product_compare_list = v.split(",")
    if o in ("-r", "--release"):
        release_compare_list = v.split(",")
    if o in ("-s", "--testsuite"):
        testsuite_compare_list = v.split(",")
    if o in ("-t", "--testcase"):
        testcase_compare_list = v.split(",")
    if o in ("-h", "--host"):
        host_compare_list = v.split(",")
    if o in ("-a", "--arch"):
        arch_compare_list = v.split(",")

read_database_init_data_pool()



if not compare_products_list:
    sys.exit(1)

print(testcase_set)
testcase_input = input("[testcase]:")
print(testsuite_set)
testsuite_input = input("[testsuite]:")
print(host_set)
host_input = input("[host]:")
print(arch_set)
arch_input = input("[arch]:")
testcase_compare_list = testcase_input.split(",")
testsuite_compare_list = testsuite_input.split(",")
host_compare_list = host_input.split(",")
arch_compare_list = arch_input.split(",")



#print(kernel_compare_list)
#print(testcase_compare_list)
#print(testsuite_compare_list)
#print(host_compare_list)
#print(release_compare_list)
#print(product_compare_list)
#print(arch_compare_list)


#print("Hello,world!")
for tc,ts,h,a in product(testcase_compare_list, testsuite_compare_list, host_compare_list, arch_compare_list):
    #print("Hello,world!")
    #print(k, tc, ts, h, r, p, a)
    for k, p, r in compare_products_list:
        if k or tc or ts or h or r or p or a:
            where_string=select_where_string(k, tc, ts, h, r, p, a)
            TestCase_gloale_list.append(read_data_perf_view_with_where(where_string))



print(TestCase_gloale_list)
    #for testcase in TestCase_gloale_list:
    #    if k == testcase.kernel_version and tc == testcase.testcase and ts == testcase.testsuite and h == testcase.host and r == testcase.release and p == testcase.product and a == testcase.arch:
    #        print(k, tc, ts, h, r, p, a)
    #        testcase.read_testcase()

#print("Global testcase list:\n", TestCase_gloale_list)

#host_input = input("[host]:")

#print(search_list(TestCase_gloale_list, lambda x: x.host == host_input))
