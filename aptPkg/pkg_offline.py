#!/usr/bin/env python2.7
# encoding: utf-8
# Copyright (c) 2016 Dilusense Inc. All Rights Reserved.

"""a file for deployment automatically"""
import os

import sys


def main(argv):

    os.system('cp -r /var/cache/apt/archives offlinePackage')

    os.system('chmod 777 -R offlinePackage/')
    
    os.system('dpkg-scanpackages offlinePackage/ /dev/null |gzip > offlinePackage/Packages.gz')

    os.system('tar cvzf offlinePackage.tar.gz offlinePackage/')

if __name__ == '__main__':

    main(argv=sys.argv)
