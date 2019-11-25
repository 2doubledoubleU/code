#!/bin/bash

# Check if you are root
if [ ! $(id -u) -eq 0 ]; then
    echo "ERROR: This program must run as root"
    exit 1
fi

IMG=${1}
# Check if the file exists
if [ ! -f ${IMG} ]; then
    echo "ERROR: File ${IMG} does not exist"
    exit 1
fi

if [ -z "$(which parted 2> /dev/null)" ]; then
    echo "ERROR: parted command not found - please install it and retry"
    exit 1
fi
if [ -z "$(which losetup 2> /dev/null)" ]; then
    echo "ERROR: losetup command not found - please install it and retry"
    exit 1
fi
if [ -z "$(which resize2fs 2> /dev/null)" ]; then
    echo "ERROR: resize2fs command not found - please install it and retry"
    exit 1
fi
if [ -z "$(which truncate 2> /dev/null)" ]; then
    echo "ERROR: truncate command not found - please install it and retry"
    exit 1
fi
if [ -z "$(which gzip 2> /dev/null)" ]; then
    echo "ERROR: gzip command not found - please install it and retry"
    exit 1
fi
INFO=$(parted -m ${IMG} unit B print | grep ext4)

NUM=$(echo ${INFO} | awk -F':' '{print $1}')
START=$(echo ${INFO} | awk -F':' '{print $2}')
OLD=$(echo ${INFO} | awk -F':' '{print $3}')
DUMMY=$(echo ${INFO} | awk -F':' '{print $4}')

START=${START::-1}
OLD=${OLD::-1}

LOOPBACK=$(losetup -f --show -o $START $IMG)
e2fsck -p -f ${LOOPBACK}
if [ ! ${?} -eq 0 ]; then
    echo "ERROR: filesystem seems corrupted"
    losetup -d ${LOOPBACK}
    exit 1
fi

INFO=$(resize2fs -P ${LOOPBACK} 2>&1)
SIZE=$(echo ${INFO} | awk -F': ' '{print $2}')
SIZE=$((${SIZE} + 1024))

resize2fs -p ${LOOPBACK} ${SIZE}

losetup -d ${LOOPBACK}
SIZE=$(( ${SIZE} * 4096 + ${START} ))

parted ${IMG} rm ${NUM}
parted -s ${IMG} unit B mkpart primary ${START} ${SIZE}

SIZE=$(( ${SIZE} + 58720257 ))
truncate -s ${SIZE} ${IMG}

