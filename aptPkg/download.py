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
    print '-d,--download: download packages'
    print '-r,--remove: uninstall packages'


def get_pkgs(requirements):

    file = open(requirements, 'r')
    pkgs = []

    print('getting require pkg...')
    try:
        stringread=file.readline()
        while stringread:
            if re.findall("#(.*?)", stringread) or re.findall("^\n(.*?)", stringread):
                pass
            else:
                stringread = re.sub(r'\n', '', stringread)
                stringread = re.sub(r'\r', '', stringread)
                stringread = re.sub(r' ', '', stringread)
                if stringread != '':
                    pkgs.append(stringread)
            stringread=file.readline()
        print('getting require pkg success!')
        return pkgs
    finally:
        file.close()

def main(argv):

    opts_full = ['--download', '--remove']
    opts_short = ['-d', '-r']
    opt = opts_short[0]
    try:
        opts, args = getopt.getopt(argv[1:], 'hdr', ['help', 'download', 'remove'])

    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    for name, value in opts:
        if name in ('-h', '--help'):
            usage()
            sys.exit(1)
        elif name in ('-d', '--download'):
            opt = opts_short[0]
        elif name in ('-r', '--remove'):
            opt = opts_short[1]
        else:
            print 'unhandled option'
            sys.exit(1)

    def uninstall_pkgs(pkgs):
        print 'uninstall exit packages...'
        for pkg in pkgs:
            print 'uninstall package: ' + pkg + '...'
            os.system('apt-get autoremove ' + pkg + ' -y')

    def download_pkgs(pkgs):
        print 'download packages...'
        for pkg in pkgs:
            print 'downloading package: ' + pkg + '...'
            os.system('apt-get -d install ' + pkg + ' -y')


    pkgs = get_pkgs('requirements.txt')

    if opt == opts_short[0]:
        print ('prepare download pkgs: ' + str(pkgs))

        uninstall_pkgs(pkgs)

        print 'clear dir: /var/cache/apt/archives...'
        os.system('rm -r /var/cache/apt/archives/*')

        download_pkgs(pkgs)

        print 'package download package...'
        os.system('python pkg_offline.py')


    elif opt == opts_short[1]:
        print ('prepare uninstall pkgs: ' + str(pkgs))
        uninstall_pkgs(pkgs)



if __name__ == '__main__':

    main(argv=sys.argv)
