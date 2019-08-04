#!/usr/bin/python
# SPDX-License-Identifier: MIT
# Copyright (c) 2014 Michael Ortmann

import struct
import sys

BOOTSECTS = 2 # 1K bootstrap
TD_SECTOR = 512
SIZEOF_LONG = 4

def get_checksum(s):
    checksum = 0

    for i in struct.unpack('>%iI' % (BOOTSECTS * TD_SECTOR / SIZEOF_LONG), s):        
        checksum += i

        if checksum > 0xffffffff:
            checksum = (checksum + 1) & 0xffffffff

    return struct.pack('>I', (~checksum) & 0xffffffff)

if len(sys.argv) != 3:
    print('USAGE: %s <bootblock.o> <bootblock.adf>' % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

f = open(filename, 'rb')
s = f.read()
f.close()

if len(s) > (BOOTSECTS * TD_SECTOR):
    print('ERROR: len of %s greater than %i bytes' % (filename, BOOTSECTS * TD_SECTOR))

s = s.ljust(BOOTSECTS * TD_SECTOR, b'\0')
checksum = get_checksum(s)
filename = sys.argv[2]

f = open(filename, 'wb')
f.write(s[0:4] + checksum + s[8:] + b'\0' * (TD_SECTOR * 9)) # min in fs-uae bootable size of adf seems to be 11 sectors
f.close()
