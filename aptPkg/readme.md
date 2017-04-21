## 一.应用场景
a.当我们需要在多台电脑安装同一个软件,并且这个软件很大，下载需要很长时间时
b.需要安装软件的ubuntu不能上网
## 二.离线安装包的制作
2.1.通过如下指令下载XXXX软件所需要的deb包

```bash
$ sudo apt-get -d install XXXXX
```

执行完上述指令后，XXXX软件的安装包就下载到了/var/cache/apt/archives目录下
2.2.生成依赖关系
1.根目录下新建一个文件夹

```bash
$ sudo mkdir offlinePackage
```

2.将下载的deb包拷贝到上述新建的文件夹下

```bash
$ sudo cp -r /var/cache/apt/archives  /offlinePackage
```

3.修改文件夹的权限，可读可写可执行

```bash
$ sudo chmod 777 -R /offlinPackage/
```

4.建立deb包的依赖关系

```bash
$ sudo dpkg-scanpackages /offlinePackage/ /dev/null |gzip >/offlinePackage/Packages.gz
```

如果出现错误：sudo: dpkg-scanpackages: command not found
则需要安装dpkg-dev工具：

```bash
$ sudo apt-get install dpkg-dev
```

2.3.打包成压缩包，以备后用

```bash
$ tar cvzf offlinePackage.tar.gz offlinePackage/
```

保存offlinePackage.tar.gz文件到U盘或服务器
## 三.在另外一台Ubuntu上离线安装

1.插入U盘或光盘，将offlinePackage.tar.gz复制到根目录下，解压

```bash
$ sudo tar -xvf offlinePackage.tar.gz
```

2.将安装包所在和源路径添加到系统源source.list

```bash
$ sudo vi /etc/apt/sources.list
deb file:/// offlinePackage/
```

然后将所有的其他deb全部注销掉（#）
注意：我们在添加之前可以先将原来的源备份以备以后使用

```bash
$ sudo cp /etc/apt/sources.list /etc/apt/sources.list.back
```

3.更新系统源

```bash
$ sudo apt-get update
```

4.离线安装
此时，在没有网络的情况下，我们就可以安装我们之间下载的XXXX软件了

```bash
$ sudo apt-get  install XXXXX
```

注意：
兼容性问题，如果我们制作安装包时，用的是64位的ubuntu，那么该离线包只能在其他64位系统上安装。
有些软件对ubuntu server和ubuntu desktop版也不兼容。总之，在什么系统下制作的离线包，就在什么系统下安装。
