#!/usr/bin/env python2.7
# encoding: utf-8
# Copyright (c) 2016 Dilusense Inc. All Rights Reserved.

"""a file for deployment automatically"""
import getopt
import os
import re

import sys


def usage():
    print 'usage:'
    print '-m,--method: The method to deploy start script. upStart/autoStart,default is upStart'


#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)


def modify_start_script_project_name(project_name, method):

    if method == 'upStart':
        file_path = project_name + '.conf'
    else:
        file_path = project_name

    file = open(file_path, 'r')
    file_object_save = None
    
    print('change project name to: ' + project_name)
    try:
        stringsave=""
        stringread=file.readline()
        while stringread:

            if method == 'upStart':
                if re.findall("description(.*?)", stringread):
                    stringread=re.sub('description(.*?)$', 'description "'+ project_name +'"', stringread)
                if re.findall("chdir /var/(.*?)", stringread):
                    stringread=re.sub('chdir /var/(.*?)$', 'chdir /var/' + project_name, stringread)
            else:
                if re.findall("project_name=(.*?)", stringread):
                    stringread=re.sub('project_name=(.*?)$', 'project_name=\'' + project_name + '\'', stringread)

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

    # upStart, autoStart
    methods = ['upStart', 'autoStart']
    method = methods[0]

    try:
        opts, args = getopt.getopt(argv[1:], 'h:', ['method='])

    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(1)
        elif o in ('-m', '--method'):
            method = a
            if method not in methods:
                print 'no method: ' + method + ' only: upStart/autoStart'
                sys.exit(1)
        else:
            print 'unhandled option'
            sys.exit(1)

    print '#################### install dependency of linux ####################'
    os.chdir(root_dir +'/aptPkg')
    os.system('python apt_install.py')


    print '#################### install dependency of python ####################'
    os.chdir(root_dir +'/pyPkg')
    os.system('./installpkg.sh')
    
    print '#################### config start script ####################'
    os.chdir(root_dir)

    if method == methods[0]:
        # upStart
        os.system('mv start_script.conf ' + project_name + '.conf')
        modify_start_script_project_name(project_name, method)
        os.system('cp ' + project_name + '.conf /etc/init/')
    else:
        # autoStart
        os.system('mv start_script ' + project_name)
        modify_start_script_project_name(project_name, method)
        os.system('cp ' + project_name + ' /etc/init.d/')
        os.system('sudo chmod 777 /etc/init.d/' + project_name)
        os.system('update-rc.d ' + project_name + ' defaults 99')

    print '#################### install & start application ####################'
    os.system('unzip -o ' + project_name + '.zip -d /var/')

    if method == methods[0]:
        os.system('sudo start ' + project_name)
    else:
        os.system('sudo service ' + project_name + ' start')



if __name__ == '__main__':

    main(argv=sys.argv)
