#!/bin/env python
# -*- encoding: utf-8 -*-
################################################
import sys
sys.path.append("..")
import config.config as config
import time,datetime
from fabric.api import *
from redis_config import redis_config

start_port = ''

host_port = ''
create_command = ''
alter_command = ''
alter_hosts = ''

#启动redis
def start_task():
    with cd(config.data_dir):
	with cd(start_port):
	    run('redis-server redis_' + start_port + '.conf') 
	    return run('netstat -tlnup|grep -v grep|grep ' + start_port + '|wc -l')


#创建集群环境
def create_task():
    with cd(config.data_dir):
	run(create_command)

#创建集群主从环境

def alter_task():
    with cd(config.data_dir):
	run(alter_command)

def uid_task():
    with cd(config.data_dir):
	with cd(start_port):
	     return run('cat nodes.conf|grep ' + alter_hosts + '|awk -F\' \' \'{print $1}\'' )
#创建主从环境
def ms_task():
    with cd(config.data_dir):
	with cd(start_port):
	   run(create_command)


def start_proc(host,port):
    global start_port
    start_port = str(port)
    env.hosts = host
    num = execute(start_task)
    while int(num.values()[0]) < 1:
	num = execute(start_task)
        time.sleep(5)



def create_environment(host):
    global start_port
    global create_command
    global alter_command
    global alter_hosts
    host_port = ''
    #开启集群并且开启复制
    if config.replicate == 'yes' and config.cluster == 'yes':
	for i in config.m_host_port:
	    host_port = host_port + ' ' + i + ':' + str(config.m_host_port[i])
	create_command = 'redis-trib.rb create  ' + host_port
        env.hosts = host
        execute(create_task)
	for k in range(0,len(config.s_host_port)):
	    start_port = str(config.m_host_port.values()[k])
            env.hosts = config.m_host_port.keys()[k]
	    alter_hosts = config.m_host_port.keys()[k]
	    uid = execute(uid_task).values()[0]
	    command_first = uid + ' ' + config.s_host_port.keys()[k] + ':' + str(config.s_host_port.values()[k]) + ' ' 
	    command_two = command_first + config.m_host_port.keys()[k] + ':' + str(config.m_host_port.values()[k])
	    alter_command = 'redis-trib.rb add-node --slave --master-id ' + command_two  
	    env.hosts = config.m_host_port.keys()[k]
            execute(alter_task)


    #开启集群未开启复制
    elif config.cluster == 'yes' and config.replicate != 'yes':
	for i in config.m_host_port:
            host_port = host_port + ' ' + i + ':' + str(config.m_host_port)
	create_command = 'redis-trib.rb create  ' + host_port
        env.hosts = host
        execute(create_task)
#只是主从复制
def replicate_only():
    global start_port
    global create_command
    if config.replicate == 'yes' and config.cluster != 'yes':
	if len(config.m_host_port) == len(config.s_host_port):
	   for i in range(0,len(config.m_host_port)):
		create_command = 'echo slaveof ' + config.m_host_port.keys()[i] + ' ' + str(config.m_host_port.values()[i]) + ' >> redis_' + str(config.s_host_port.values()[i]) + '.conf'
		env.hosts = config.s_host_port.keys()[i]
		start_port = str(config.s_host_port.values()[i])
		execute(ms_task)	
