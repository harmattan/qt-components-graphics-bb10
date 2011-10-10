#!/usr/bin/python

"""
This scripts inspect a set of dirs and creates a file wich contains
a list of files contained in those dirs with the following structure:
number,name,width,height,location
"""

from itertools import ifilter
from os import walk, path, popen
from md5 import new as md5

IMGSIZE="identify -format '%[fx:w],%[fx:h]' "

def traversedir(where):
    for root, dirs, candidates in walk(where):
        for filename in ifilter(lambda x: '.' in x, candidates):
            yield(path.join(root, filename))

def parse_tree(where, theme={}):
    for abspath in ifilter(lambda x: '.' in x, traversedir(where)):
        if not abspath.endswith(('.svg', '.jpg', '.png')):
            continue
        width, _, height = next(popen(IMGSIZE + abspath)).strip().rpartition(',')
        basename, _, extension = abspath.rpartition('.')
        theme.setdefault(path.basename(basename), []).append((str(width), str(height), extension, abspath[len(where):],))
    return theme

def compare(file_a, file_b):
    with file(file_a ,'rb') as f1: 
        with file(file_b, 'rb') as f2:
            return md5(f1.read()).digest() == md5(f2.read()).digest()

if __name__ == '__main__':

    import sys
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: fetch.py <destination> <target_dir>..\n")
        exit(255)

    candidates = {}    
    for value in sys.argv[2:]:
        candidates = parse_tree(value, candidates)

    with file(sys.argv[1], "w") as dest:
        duplicates, current = {}, 1
        for key, values in candidates.iteritems():
            if len(values) > 1:
                duplicates[key] = values
            else:
                dest.write(str(current) + "," + ",".join(values[0]) + "\n")
                current += 1

    print "duplicates: " + str(int((len(duplicates) * 100) / len(candidates))) + "% (" + str(len(duplicates)) + ")"
    


    
    
