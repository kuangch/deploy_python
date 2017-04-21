#!/usr/bin/env python2.7
# encoding: utf-8
# Copyright (c) 2016 Dilusense Inc. All Rights Reserved.

"""a file for deployment automatically"""
import os
import re
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

def modify_start_script_project_name(project_name):
    file_path = project_name + '.conf'
    file = open(file_path, 'r')
    file_object_save = None
    
    print('change project name to: ' + project_name)
    try:
        stringsave=""
        stringread=file.readline()
        while stringread:
            if re.findall("description(.*?)", stringread):
                stringread=re.sub('description(.*?)$','description "'+ project_name +'"',stringread)
            if re.findall("chdir /var/(.*?)", stringread):
                stringread=re.sub('chdir /var/(.*?)$','chdir /var/' + project_name,stringread)

            stringsave=stringsave+stringread
            stringread=file.readline()

        file_object_save = open(file_path, 'w')
        file_object_save.write(stringsave)
        
        print('modify start script file success')
    finally:
        file.close()
        if file_object_save:
            file_object_save.close()

def main(argv):

    project_name = 'web_frame_flask'
    
    root_dir = str(cur_file_dir())

    print '#################### install dependency of linux ####################'
    os.chdir(root_dir +'/aptPkg')
    os.system('python apt_install.py')
    
    
    print '#################### install dependency of python ####################'
    os.chdir(root_dir +'/pyPkg')
    os.system('./installpkg.sh')
    
    print '#################### copy start script to /etc/init/ ####################'
    os.chdir(root_dir)
    
    os.system('mv start_script.conf '+ project_name +'.conf')
    modify_start_script_project_name(project_name)
    os.system('cp '+ project_name +'.conf /etc/init/')
    
    print '#################### install & start application ####################'
    os.system('unzip -o '+ project_name +'.zip -d /var/')
    os.system('sudo start ' + project_name)


if __name__ == '__main__':

    main(argv=sys.argv)
