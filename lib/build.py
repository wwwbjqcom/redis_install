#!/bin/env python
# -*- encoding: utf-8 -*-
################################################
import sys
sys.path.append("..")
import config.config as config
from install_pro import install_proc
from install_pro import install_gem
import time,datetime
from fabric.api import *
import redis_start

##host去重
def distinct_host():
        host_list = []
        for i in config.m_host_port:
            if i not in host_list:
                host_list.append(i)
        for k in config.s_host_port:
            if k not in host_list:
                host_list.append(k)
        return host_list


class redis_input:
    def __init__(self):
	self.replicate = config.replicate
        self.cluster = config.cluster
        self.m_host_port = config.m_host_port
        self.s_host_port = config.s_host_port
	self.redis_para = config.redis_para
	self.redis_name = config.redis_name
	self.zlib_name = config.zlib_name
	self.ruby_name = config.ruby_name
	self.rubygems_name = config.rubygems_name
	self.redis_gem_name = config.redis_gem_name
    def redis_build(self):
	if self.cluster == 'yes':
	   print "5秒以后开始编译安装集群！"
	   i=5
	   while (i > 0):
		print "安装倒计时%d " % i
		i = i - 1
		time.sleep(1)

	   pack_name_list = {}
	   pack_name_list['zlib_command'] = self.zlib_name
	   pack_name_list['ruby_command'] = self.ruby_name
	   pack_name_list['rubygems_command'] = self.rubygems_name
	   pack_name_list['redis_command'] = self.redis_name
		
	   command_list = {}
	   command_list['zlib_command'] = './configure && make && make install'
	   command_list['ruby_command'] = './configure && make && make install && cp ruby /usr/local/bin'
	   command_list['rubygems_command'] = 'ruby setup.rb && cp bin/gem /usr/local/bin'
	   command_list['redis_gem_command'] = 'gem install -l ' + config.redis_gem_name
	   command_list['redis_command'] = 'make && make install'
	   for i in command_list:
		if i == 'redis_gem_command':
		   install_gem(self.redis_gem_name,command_list[i],self.m_host_port,self.s_host_port,distinct_host())
		else:
	   	   install_proc(pack_name_list[i],command_list[i],self.m_host_port,self.s_host_port,distinct_host())
	  
	elif self.cluster == 'no':
	   print "该安装的是非集群环境，5秒以后开始编译！"
           i=5
           while (i > 0):
                print "安装倒计时%d " % i
                i = i - 1
                time.sleep(1)
	   command = 'make && make install'
	   pack_name = self.redis_name
	   install_proc(pack_name,command,self.m_host_port,self.s_host_port,distinct_host())
	else:
	   print "config.cluster配置有误！"

    def redis_start(self):
	if self.cluster != 'yes' and self.replicate == 'yes':
                redis_start.replicate_only()
	for i in self.m_host_port:
	    redis_start.start_proc(i,self.m_host_port[i])
	for k in self.s_host_port:
	    redis_start.start_proc(k,self.s_host_port[k])
	
	redis_start.create_environment(self.m_host_port.keys()[0])

















