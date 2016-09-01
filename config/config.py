#!/bin/env python
# -*- encoding: utf-8 -*-
###############################################

base_dir = '/home/xiaozhong/redis_install'

#----运行用户访问远程服务器密码
#password = ''

#----是否是集群模式[yes/no]
cluster = 'no'

#----是否开启主从
replicate = 'no'

#----设置需要安装redis的IP和端口,m_host_port和s_host_port顺序对应主从关系
#----未开启主从模式可以不填s_host_port
m_host_port = {'172.31.10.102':27031}
s_host_port = {}

#----安装路径
install_dir = '/usr/local/src'

#----redis数据目录
data_dir = '/home/xiaozhong/redis'

#----redis安装文件路径及名称
redis_name = 'redis-3.2.0.tar.gz'
zlib_name = 'zlib-1.2.8.tar.gz'
ruby_name = 'ruby-2.1.9.tar.gz'
rubygems_name = 'rubygems-2.6.4.tgz'
redis_gem_name = 'redis-3.2.0.gem'

#----redis全局配置参数
str = """daemonize yes
#cluster-enabled yes
#cluster-config-file nodes.conf
#cluster-node-timeout 50
slave-read-only yes
repl-backlog-size 10M
repl-backlog-ttl 3600
maxclients 5000
maxmemory 100m
appendonly yes
save ""
appendfsync everysec
aof-load-truncated yes
slowlog-log-slower-than 1000
slowlog-max-len 128
aof-rewrite-incremental-fsync yes
auto-aof-rewrite-percentage 100"""
redis_para = str.split("\n")


