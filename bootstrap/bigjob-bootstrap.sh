#!/bin/bash

env
whoami

<<<<<<< HEAD
ANACONDA_BIGJOB_DIRECTORY=$HOME/.bigjob/python

BIGJOB_DIRECTORY=./.bigjob/python

echo "BigJob directory: $BIGJOB_DIRECTORY" 
if [ -d $BIGJOB_DIRECTORY ]  || [ -d $ANACONDA_BIGJOB_DIRECTORY ]
then
    echo "Using existing BigJob version"
elif   [ -d $ANACONDA_BIGJOB_DIRECTORY ]
then
    echo "Using existing BigJob (Anaconda) version"
    BIGJOB_DIRECTORY=ANACONDA_BIGJOB_DIRECTORY
#BIGJOB_DIRECTORY=./.bigjob/python
#echo "BigJob directory: $BIGJOB_DIRECTORY"
#if [ -d $BIGJOB_DIRECTORY ]
#then
#    echo "Using existing BigJob version"
else
    mkdir -p $BIGJOB_DIRECTORY
    BOOTSTRAP_DOWNLOAD_CMD="curl -OL --insecure -s https://raw.github.com/saga-project/BigJob/develop/bootstrap/bigjob2-bootstrap.py"
    echo "## Downloading BigJob"
    echo $BOOTSTRAP_DOWNLOAD_CMD
    $BOOTSTRAP_DOWNLOAD_CMD
    OUT=$?
    if [ $OUT -ne 0 ];then
        echo "Couldn't download BigJob. Exiting"
        exit 1
    fi
    echo "## Install BigJob"    
    INSTALL_CMD="python bigjob-bootstrap.py $BIGJOB_DIRECTORY"
    echo "Command: "$INSTALL_CMD
    $INSTALL_CMD
    OUT=$?
    if [ $OUT -ne 0 ];then
        echo "Couldn't install BigJob. Exiting"
        exit 1
    fi
fi

echo "Activate BigJob environment"
ACTIVATE_VIRTUALENV_CMD=". $BIGJOB_DIRECTORY/bin/activate"
echo $ACTIVATE_VIRTUALENV_CMD
$ACTIVATE_VIRTUALENV_CMD
OUT=$?
if [ $OUT -ne 0 ];then
    echo "Couldn't activate BigJob virtualenv. Exiting"
    exit 1
fi

echo "Start BigJob Agent"
START_BIGJOB_AGENT_CMD="python -m bigjob.bigjob_agent  $*"
echo $START_BIGJOB_AGENT_CMD
$START_BIGJOB_AGENT_CMD
OUT=$?
if [ $OUT -ne 0 ];then
    echo "Couldn't start BigJob. Exiting"
    exit 1
fi
