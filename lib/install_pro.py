#!/bin/env python
# -*- encoding: utf-8 -*-
################################################
import sys
sys.path.append("..")
import config.config as config
import time,datetime
from fabric.api import *
from redis_config import redis_config

str_pack = ''
pack_name = ''
command = ''
def task_1():
    put(config.base_dir + '/' + 'install_pack' + '/' + str_pack,config.install_dir)
    with cd(config.install_dir):
         run('tar zxvf ' + str_pack)
	 run('rm -rf ' + str_pack)
         with cd(pack_name):
              run(command)

def task_2():
    put(config.base_dir + '/' + 'install_pack' + '/' + str_pack,config.install_dir)
    with cd(config.install_dir):
         run(command)
	 

def task_ln():
    with cd(config.install_dir):
	with cd(pack_name + '/src'):
	     run('rm -rf /usr/local/sbin/redis-cli')
	     run('rm -rf /usr/local/sbin/redis-server')
	     run('rm -rf /usr/local/sbin/redis-trib.rb')
	     run('cp  redis-cli /usr/local/sbin/redis-cli')
	     run('cp  redis-server /usr/local/sbin/redis-server')
	     run('cp  redis-trib.rb /usr/local/sbin/redis-trib.rb')


##安装包编译
def install_proc(pack,build_command,host,s_host,host_list):
    global str_pack
    global command
    global pack_name
    command = str(build_command)
    str_pack = str(pack)
    if pack == config.rubygems_name:
	pack_name = str(pack.split('.tgz')[0])
    else:
        pack_name = str(pack.split('.tar')[0])
    for i in host:
	if i not in host_list:
	   print "对应master IP已执行过安装，只执行配置"
	   if pack == config.redis_name:
	      redis_config(i,host[i])
	else:
           env.hosts=i
           execute(task_1)
           if pack == config.redis_name:
              redis_config(i,host[i])
	      execute(task_ln)
           host_list.remove(i)
    for k in s_host:
        if k not in host_list:
           print "对应slave IP已执行过安装，只执行配置"
           if pack == config.redis_name:
              redis_config(k,s_host[k])
	else:
           env.hosts=k
           execute(task_1)
           if pack == config.redis_name:
              redis_config(k,s_host[k])
	      execute(task_ln)
           host_list.remove(k)
	print "配置完成！ok！"
    
	
##redis_gem 编译函数
def install_gem(pack,build_command,host,s_host,host_list):
    global str_pack
    global command
    command = str(build_command)
    str_pack = str(pack)
    for i in host:
	if i in host_list:
           env.hosts=i
           execute(task_2)
	   host_list.remove(i)
    
    for k in s_host:
        if k in host_list:
           env.hosts=k
           execute(task_2)
           host_list.remove(k)
    
