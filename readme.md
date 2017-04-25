## 部署说明

文中所有xxx代表项目名称（和部署包下面的web应用程序zip包的名称相同，是根据zip包名称自动生成的）

#### 一.环境要求

1.Ubuntu 14

2.python 2.7 (Ubuntu 14操作系统默认自带)

#### 二.部署步骤

1.将部署包解压至要部署的服务器任意目录下

2.cd到解压的部署包根目录下，执行部署命令
```bash
$ sudo python deploy.py

# 部署过程大概 1-2分钟，最后出现
root@ubuntu:~/deploy_python# xxx start/running, process 7196
或者
root@ubuntu:~/deploy_python# nohup: redirecting stderr to stdout

表示部署成功，浏览器输入 ip:9101查看是否部署成功
```
* 注意，安装离线包的过程会更换apt-get源完成离线包安装后要换回系统默认源并update，如果部署机器可以连外网将会需要几分钟时间更新源影响部署速度，建议断开外网连接

3.选择启动脚本类型

由于部分linux版本不支持upstart方式的启动脚本。
执行部署脚本命令时可以传递 ```--method``` 参数用于选择生成启动脚本的方式
有两种模式（默认是 autoStart）：
`upStart`：启动脚本将会生成到 /etc/init/xxx.conf
服务控制：
```bash
#启动
$ start xxx
#停止
$ stop xxx
#停止
$ stop xxx
$ start xxx
```
`autoStart`：启动脚本将会生成到 /etc/init.d/xxx, 并在/etc/rcX.d/下面生成自启动配置
服务控制：
```bash
#启动
$ service xxx start
#停止
$ service xxx stop
#重启
$ service xxx restart
```

如果要部署的linux主机不支持upstart，部署命令为：
```bash
$ sudo python deploy.py --method=autoStart
```