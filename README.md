# redis_install


redis集群、单节点、主从一键安装小脚本</br>

注意事项：</br>
1、config/config.py 为所有配置项的配置文件</br>
2、base_dir 为该工程所在目录，结尾部别带'/'</br>
3、开启主从必须保证m_host_port、s_host_port长度一直</br>
4、安装之前确保所有节点已安装make、gcc、gcc-c++依赖包</br>
5、安装之前确保所有节点root用户能免密码登陆</br>
6、install_dir、data_dir需在安装开始前创建目录</br>
7、配置参数请配置在str项，端口会自动从m_host_port、s_host_port提取</br>
8、cluster选项为集群模式</br>
9、replicate选项开启主从</br>
10、安装包在install_pack文件夹下</br>
11、可以在config.py中修改安装包名称</br>
12、配置完成直接运行main.py</br>
13、在执行安装脚本的服务器需安装python 的 fabric 模块</br>
