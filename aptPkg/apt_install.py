#!/usr/bin/env python2.7
# encoding: utf-8
# Copyright (c) 2016 Dilusense Inc. All Rights Reserved.

"""a file for deployment automatically"""
import os

import sys


def main(argv):

    pkgs = [
        'python-dev',
        'libmysqld-dev',
        'zip',
        'python-pip'
    ]
    print 'unzip offline package...'
    os.system('tar -xvf offlinePackage.tar.gz -C /')

    print 'backup sources.list...'
    os.system('mv /etc/apt/sources.list /etc/apt/sources.list.back')

    print 'modify sources.list...'
    os.system('echo "deb [trusted=yes] file:/// offlinePackage/" > /etc/apt/sources.list')
    os.system('cat /etc/apt/sources.list')

    print 'update sources.list...'
    os.system('apt-get update')

    for pkg in pkgs:
        print 'install '+pkg+'...'
        os.system('apt-get install '+pkg+' -y')

    print 'remove offline package...'
    os.system('rm -r /offlinePackage')

    print 'restore sources.list...'
    os.system('mv /etc/apt/sources.list.back /etc/apt/sources.list')

    print 'update sources.list...'
    os.system('apt-get update')


if __name__ == '__main__':

    main(argv=sys.argv)
