#!/bin/bash

uninstall(){
    echo "uninstall python pkg..."
	pip uninstall -r requirements.txt -y
}

install(){
    echo "install python pkg..."
	pip install --no-index --find-links=pypkg -r requirements.txt
}

download(){
    echo "download python pkg..."
	pip install --download pypkg -r requirements.txt -t100000
}

case "$1" in
    install)
        install
        ;;
    download)
        download
        ;;
    uninstall)
        uninstall
        ;;
    *)
        install
esac

exit $RETVAL

	
