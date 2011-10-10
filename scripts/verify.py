#!/usr/bin/python

from itertools import ifilter
from os import walk, path
from md5 import new as md5

def traversedir(where):
    for root, dirs, candidates in walk(where):
        for filename in ifilter(lambda x: '.' in x, candidates):
            yield(path.join(root, filename))

def parse_tree(where, theme={}):
    for abspath in ifilter(lambda x: '.' in x, traversedir(where)):
        if not abspath.endswith(('.svg', '.png', '.jpg',)):
            continue
        basename, _, extension = abspath.rpartition('.')
        theme.setdefault(path.basename(basename), []).append((abspath, extension,))
    return theme

def compare(file_a, file_b):
    with file(file_a ,'rb') as f1: 
        with file(file_b, 'rb') as f2:
            return md5(f1.read()).digest() == md5(f2.read()).digest()

if __name__ == '__main__':

    import sys
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: merge.py <origin_dir> <target_dir>..\n")
        exit(255)

    candidates = {}    
    theme = parse_tree(sys.argv[1])
    for value in sys.argv[2:]:
        print value
        candidates = parse_tree(value, candidates)

    missing, match = [], []
    for key, values in theme.iteritems():
        if key not in candidates:
            missing.append(values[0])
        else:
            for value in candidates[key]:
                if values[0][1] != value[1]:
                    continue
                if compare(values[0][0], value[0]):
                    match.append((values[0][0], values[0],))
                    break
            else:
                missing.append(values[0])

    print "match: " + str(int((len(match) * 100) / len(theme))) + "% (" + str(len(match)) + ")"



    
    
