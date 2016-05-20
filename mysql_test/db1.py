#!/usr/bin/env python3

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import mysql.connector

import collections

from collections import OrderedDict

from mysql.connector import errorcode

from itertools import product

import urllib.request

from urllib.error import HTTPError

import io

import os

import re

import sys

import getopt

import statistics

from configparser import ConfigParser
from configparser import RawConfigParser
import configparser

#用于记录哪些产品参与对比
compare_products_list = list()

kernel_compare_list = list()
product_compare_list = list()
release_compare_list = list()
testcase_compare_list= list()
testsuite_compare_list= list()
arch_compare_list = list()
host_compare_list = list()


TestCase_gloale_list = list()

def read_statistics_list_make_statistics_data(a_list):
    data=OrderedDict()
    for l in a_list:
        data[l.name]=l.values()
    #data = {
    #        'adfas': [123,123,123,123,123],
    #        'axxxdfas': [123,123,123,123,123],
    #        'a234s': [123,123,123,123,123],
    #        'ad__s': [123,123,123,123,123],
    #        }
    return data






class benchmark():
    """flag mean that value is more bigger more better or more smaller more better."""
    def __init__(self, name, value, flag):
        self.name = name
        self.value = value
        self.flag = flag

    def __repr__(self):
        #return ":".join([self.name, self.value])
        return "<benchmark object>"

    def __add__(self, other):
        if (self.name != other.name):
            raise TypeError
        if (self.flag != other.flag):
            raise TypeError
        value = self.value + other.value
        return benchmark(self.name, value, self.flag)

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
    #print(where_string)
    if tc:
        if start == False:
            where_string="".join([where_string, "and"])
        where_string="".join([where_string, " `testcase` = '"+tc+"' "])
        start = False
    #print(where_string)

    if ts:
        if start == False:
            where_string="".join([where_string, "and"])
        where_string="".join([where_string, " `testsuite` = '"+ts+"' "])
        start = False
    #print(where_string)

    if h:
        if start == False:
            where_string="".join([where_string, "and"])
        where_string="".join([where_string, " `host` = '"+h+"' "])
        start = False
    #print(where_string)

    if r:
        if start == False:
            where_string="".join([where_string, "and"])
        where_string="".join([where_string, " `release` = '"+r+"' "])
        start = False
    #print(where_string)
    if p:
        if start == False:
            where_string="".join([where_string, "and"])
        where_string="".join([where_string, " `product` = '"+p+"' "])
        start = False
    #print(where_string)
    if a:
        if start == False:
            where_string="".join([where_string, "and"])
        where_string="".join([where_string, " `arch` = '"+a+"' "])
    #print(where_string)
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


        #search_list(testcase_list, lambda x: print(x.testsuite, x.testcase, x.host, x.kernel_long_version, x.product, x.release, x.benchmark))
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
            self.benchmark_bonniepp()
            return
        if self.testcase == 'bonnie++-fsync':
            self.benchmark_bonniepp()
            return
            return
        if self.testcase == 'dbench4-async':
            return
        if self.testcase == 'dbench4-fsync':
            return
        if self.testcase == 'kernbench':
            self.benchmark_kernbench()
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
        self.benchmark = list()
        pattern=re.compile(b'Max Jobs per Minute ([0-9].*\.*[0-9]*)')
        for line in urllib.request.urlopen(self.log_url+"/"+self.testcase):
            m = pattern.match(line)
            if m:
                value=str(m.group(1), 'utf-8')
                self.benchmark.append(benchmark('Jobs_per_Minute', value, 1))
                continue

    def benchmark_bonniepp(self):
        self.benchmark = list()
        pattern=re.compile(b'^Machine')
        with urllib.request.urlopen(self.log_url+"/"+self.testcase) as page:
            g = io.BufferedReader(page)
            t = io.TextIOWrapper(g, 'utf-8')
            for line in t:
                pattern=re.compile('Machine .*Size')
                m = pattern.match(line)
                print(line)
                if m:
                    line=next(t).split()
                    self.benchmark.append(benchmark('Sequential_Output#Per_char#K/s', line[2], 1))
                    self.benchmark.append(benchmark('Sequential_Output#Block#K/s', line[4], 1))
                    self.benchmark.append(benchmark('Sequential_Output#Rewrite#K/s', line[6], 1))
                    self.benchmark.append(benchmark('Sequential_Input#Per_char#K/s', line[8], 1))
                    self.benchmark.append(benchmark('Sequential_Input#Block#K/s', line[10], 1))
                    self.benchmark.append(benchmark('Random#Seeks#sec', line[12], -1))
                    break










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

        if compare_products_list:
            return

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

optlist, args = getopt.getopt(args,'k:p:r:s:t:h:a:',['kernel=', 'product=', 'release=', 'testsuite=', 'testcase=', 'host=', 'arch='])

for o, v in optlist:
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

if kernel_compare_list and product_compare_list and release_compare_list:
    print("Choosed product set:")
    for k, p, r in zip(kernel_compare_list, product_compare_list, release_compare_list):
        print(",".join([k,p,r]))
        compare_products_list.append([k,p,r])

read_database_init_data_pool()



if not compare_products_list:
    sys.exit(1)

print(testcase_set)
if not testcase_compare_list:
    testcase_input = input("[testcase]:")
    testcase_compare_list = testcase_input.split(",")
print(testsuite_set)
if not testsuite_compare_list:
    testsuite_input = input("[testsuite]:")
    testsuite_compare_list = testsuite_input.split(",")
print(host_set)
if not host_compare_list:
    host_input = input("[host]:")
    host_compare_list = host_input.split(",")
print(arch_set)
if not arch_compare_list:
    arch_input = input("[arch]:")
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



print("TestCase_gloale_list=", TestCase_gloale_list)

#==========================STAGE II============================
class statistics_node():
    """this class will make a statistics node for the list, the list will be use for statistics table"""
    def __init__(self, _list):
        self.name = "/".join([_list[0].product, _list[0].release, _list[0].kernel_long_version])
        self.data = _list
        self.benchmarks = OrderedDict()
        self.benchmarks_init()
        #self.print_benchmarks()

    def benchmarks_init(self):
        _tmp_dict=dict()
        for tc in self.data:
            for bm in tc.benchmark:
                if bm.name in _tmp_dict:
                    _tmp_dict[bm.name].append(float(bm.value))
                else:
                    _tmp_dict[bm.name] = [float(bm.value)]
        for k, v in _tmp_dict.items():
            self.benchmarks[k]=OrderedDict()
            self.benchmarks[k]['mean']=statistics.mean(v)
            self.benchmarks[k]['sum']=sum(v)
            self.benchmarks[k]['max']=max(v)
            self.benchmarks[k]['min']=min(v)
            self.benchmarks[k]['stddev']=statistics.stdev(v)
            self.benchmarks[k]['count']=len(v)


    def print_benchmarks(self):
        print(self.benchmarks)
    def __repr__(self):
        return self.name

    def values(self):
        self.indexs=list()
        values=list()
        for k,v in self.benchmarks.items():
            for k1,v1 in v.items():
                self.indexs.append(str(k)+'/'+str(k1))
                values.append(v1)

        #print(','.join(str(self.benchmarks[k] for k in self.benchmarks.keys())))
        return values

    def __str__(self):
        self.indexs=list()
        values=list()
        for k,v in self.benchmarks.items():
            for k1,v1 in v.items():
                self.indexs.append(str(k)+str(k1))
                values.append(v1)

        #print(','.join(str(self.benchmarks[k] for k in self.benchmarks.keys())))
        return str(values)

    def mean(self):
        pass

    def _sum(self, _list):
        pass
    def stddev(self, _list):
        pass
    def cov(self, _list):
        pass
    def _min(self, _list):
        pass
    def _max(self, _list):
        pass

product_statistics_lists=list()
for l in TestCase_gloale_list:
    #print(compare_products_list[TestCase_gloale_list.index(l)][0] == l[0].kernel_version)
    product_statistics_lists.append(statistics_node(l))

#print(product_statistics_lists)

data=read_statistics_list_make_statistics_data(product_statistics_lists)

pd.set_option('display.width', 1000)
football = pd.DataFrame(data, index=product_statistics_lists[0].indexs)
print(football)

    #for testcase in TestCase_gloale_list:
    #    if k == testcase.kernel_version and tc == testcase.testcase and ts == testcase.testsuite and h == testcase.host and r == testcase.release and p == testcase.product and a == testcase.arch:
    #        print(k, tc, ts, h, r, p, a)
    #        testcase.read_testcase()

#print("Global testcase list:\n", TestCase_gloale_list)

#host_input = input("[host]:")

#print(search_list(TestCase_gloale_list, lambda x: x.host == host_input))
