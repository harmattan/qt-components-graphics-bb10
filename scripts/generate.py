#!/usr/bin/python

"""
This scripts, based on a source file, create missing images according to
source data
"""
CONVERT="convert -size {width}x{height} xc:white -fill none -gravity center -stroke black -annotate 0 '{iid}' "

from itertools import ifilter
from shutil import copy
from md5 import new as md5
from os import walk, path, makedirs, system

def parse_file(where, theme={}):
    with file(where, "r") as f:
        for line in f:
            yield tuple(line.strip().split(','))
            
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        sys.stderr.write("Usage: create.py <source_file> <result_file> <result_dir>\n")
        exit(255)

    candidates, generated = [], []
    with file(sys.argv[2], "w") as dest:
        for value in parse_file(sys.argv[1]):
            destination = path.join(sys.argv[3], value[4].rpartition('.')[0])
            candidates.append(value)
            for exts in ('.png', '.jpg', '.svg'):
                if path.isfile(destination + exts):
                    break
            else:
                destination = destination + '.' + value[3]
                try:
                    makedirs(path.dirname(destination))
                except:
                    pass
                system(CONVERT.format(width=value[1], height=value[2], iid=value[0]) + destination)
                dest.write(",".join(value) + '\n')
                generated.append(value)


    print "generated:   " + str(int(((len(candidates) - len(generated)) * 100) / len(candidates))) + "% (" + str(len(candidates) - len(generated)) + ")"
    


    
    
