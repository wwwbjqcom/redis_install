#!/bin/env python
# -*- encoding: utf-8 -*-
################################################
import sys
sys.path.append("..")
import config.config as config
import time,datetime
from fabric.api import *




data_port = ''
bind_host = ''
##复制配置全局配置文件
def task_1():
    #put(config.base_dir + '/' + 'install_pack/redis_global.conf',config.data_dir + '/' + data_port)
    with cd(config.data_dir):
	run('mkdir ' + data_port)
	put(config.base_dir + '/' + 'install_pack/redis_global.conf',config.data_dir + '/' + data_port)
	with cd(data_port):
	    run('mv redis_global.conf redis_' + data_port + '.conf')
            run('echo "port ' + data_port + '" >> redis_' + data_port + '.conf')
	    run('echo "bind ' + bind_host +'" >> redis_' + data_port + '.conf')
	    run('echo \'appendfilename  "appendonly-' + data_port + '.aof"\' >> redis_' + data_port + '.conf')
	


def redis_config(host,host_port):
	global data_port
	global bind_host
	bind_host = host
	data_port = str(host_port)
	env.hosts = host
	execute(task_1)
    
