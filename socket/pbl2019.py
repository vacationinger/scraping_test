#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pbl2019.py - Support module for PBL2019
#

import uuid
import hashlib


def genkey(token_str):
    m = hashlib.sha256()
    m.update(token_str.encode('utf-8'))
    m.update(("%x" % uuid.getnode()).encode('utf-8'))
    key_str = m.hexdigest()
    return key_str


def repkey(token_str, filename):
    m = hashlib.sha256()
    m.update(token_str.encode('utf-8'))
    m.update(("%x" % uuid.getnode()).encode('utf-8'))
    key_str = m.hexdigest()

    n = hashlib.sha256()
    n.update(key_str.encode('utf-8'))
    try:
        f = open(filename, 'rb')
        while True:
            b = f.read(1024)
            if b == b'':
                break
            n.update(b)
    except OSError:
        raise
    repkey_str = key_str + n.hexdigest()
    return repkey_str


def keycheck(repkey_data, filename):
    genkey_data = repkey_data[:64]
    received_digest = repkey_data[64:]
    n = hashlib.sha256()
    n.update(genkey_data.encode('utf-8'))
    try:
        f = open(filename, 'rb')
        while True:
            b = f.read(1024)
            if b == b'':
                break
            n.update(b)
    except OSError:
        raise
    our_digest = n.hexdigest()
    if our_digest == received_digest:
        return True
    return False


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        sys.exit("Usage: {0} token_str file_name1 file_name2".
                 format(sys.argv[0]))
    token_str = sys.argv[1]
    file_name1 = sys.argv[2]
    file_name2 = sys.argv[3]
    genkey_data = genkey(token_str)
    print("genkey: %s" % genkey_data)
    repkey_data = repkey(token_str, file_name1)
    print("repkey(file1): %s" % repkey_data)
    print("keycheck(repkey(file1), file1): %s" %
          keycheck(repkey_data, file_name1))
    print("keycheck(repkey(file1), file2): %s" %
          keycheck(repkey_data, file_name2))
    print("genkey retrieved from repkey %s" % repkey_data[:64])
