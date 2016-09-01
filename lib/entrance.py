#!/bin/env python
# -*- encoding: utf-8 -*-
################################################
import sys,os
sys.path.append("..")
import config.config as config
import time,datetime
from os.path import exists
from fabric.api import *
from build import redis_input

##生成redis全局配置文件
def redis_config():
        redis_para = eval(str(config.redis_para))
        file_name = config.base_dir + '/install_pack/redis_global.conf'
        if exists(file_name):
           os.remove(file_name)
           file_object = open(file_name,'a')
           for i in range(0,len(redis_para)):
                file_object.write(redis_para[i])
                file_object.write('\n')
           file_object.close()
        while not exists(file_name):
           file_object = open(file_name,'a')
           for i in range(0,len(redis_para)):
                file_object.write(redis_para[i])
                file_object.write('\n')
           file_object.close()


def entrance():
	redis_config()
	re = redis_input()
	re.redis_build()
	re.redis_start()
