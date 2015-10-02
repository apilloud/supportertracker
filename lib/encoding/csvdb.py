'''
This module has helpers for importing csv.
'''

import csv
import itertools
import multiprocessing
import sys

import jsonld
import protocol


def decode_field(field):
    try:
        # 85% chance it's UTF8 or ASCII
        field.decode('utf_8')
        return field
    except UnicodeDecodeError:
        # cp1252 is a superset of ISO-8859-1
        # 8.5% chance it's one of those
        return field.decode('cp1252').encode('utf_8')


def mapper(linedict):
    decodedict = {}
    for key, value in linedict.items():
        if value:
            decodedict[key] = decode_field(value)
    record = jsonld.LinkedDict(decodedict)
    return (record.id(), str(record))


def isdup(line, known):
    if line in known:
        return True
    known[line] = True
    return False


def process(filename):
    infile = open(filename)
    outfile = open(filename + '.std', 'w')

    fiter = iter(infile)
    sample = fiter.next()
    for line in fiter:
        if not line.strip():
            continue
        sample = sample + line
        if len(sample) >= 4096:
            break
    dialect = csv.Sniffer().sniff(sample)
    infile.seek(0)

    csviter = iter(csv.reader(infile, dialect))
    header = csviter.next()

    dictiter = iter(csv.DictReader(infile, fieldnames=header, dialect=dialect))

    if multiprocessing.cpu_count() > 1:
        pool = multiprocessing.Pool()
        mapiter = pool.imap(mapper, dictiter, 4096)
    else:
        mapiter = itertools.imap(mapper, dictiter)

    known = {}
    wprotocol = protocol.PostgresProtocol()

    for hexhash, rawjson in mapiter:
        if isdup(hexhash, known):
            continue
        if rawjson:
            outfile.write(wprotocol.write(hexhash, rawjson) + '\n')

    infile.close()
    outfile.close()
