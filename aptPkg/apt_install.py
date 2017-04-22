#!/usr/bin/env python2.7
# encoding: utf-8
# Copyright (c) 2016 Dilusense Inc. All Rights Reserved.

"""a file for deployment automatically"""
import os
import subprocess

import sys

#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

def main(argv):

    pkg_dir = str(cur_file_dir())[1:]

    print 'unzip offline package...'
    os.system('tar -xvf offlinePackage.tar.gz -C /')

    print 'backup sources.list...'
    os.system('mv /etc/apt/sources.list /etc/apt/sources.list.back')

    print 'modify sources.list...'
    os.system('echo "deb [trusted=yes] file:/// offlinePackage/" > /etc/apt/sources.list')
    os.system('cat /etc/apt/sources.list')

    print 'update sources.list...'
    os.system('apt-get update')

    print 'install python-dev...'
    os.system('apt-get install python-dev -y')

    print 'install libmysqld-dev...'
    os.system('apt-get install libmysqld-dev -y')
    
    print 'install zip...'
    os.system('apt-get install zip -y')

    print 'install pip...'
    os.system('apt-get install python-pip -y')
    
    print 'remove offline package...'
    os.system('rm -r /offlinePackage')

    print 'restore sources.list...'
    os.system('mv /etc/apt/sources.list.back /etc/apt/sources.list')

    print 'update sources.list...'
    os.system('apt-get update')


if __name__ == '__main__':

    main(argv=sys.argv)
