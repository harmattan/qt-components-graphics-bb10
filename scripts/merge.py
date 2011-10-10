#!/usr/bin/python

"""
This scripts, based on a source file, inspect a set of dirs and fetch files
required by this source file in order of preference. In case of duplicates, 
more important files are fetched in order of preference from left ro right
"""

from itertools import ifilter
from shutil import copy
from md5 import new as md5
from os import walk, path, popen, makedirs

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
        theme.setdefault(path.basename(basename), []).append((str(width), str(height), extension, abspath, where[:30],))
    return theme

def parse_file(where, theme={}):
    with file(where, "r") as f:
        for line in f:
            values = tuple(line.split(','))
            key, _, _ = path.basename(values[4]).strip().rpartition('.')
            theme[key] = values
    return theme
            
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        sys.stderr.write("Usage: fetch.py <source_file> <result_file> <highest_pref_dir>..<lowest_pref_dir>\n")
        exit(255)

    candidates = {}
    theme = parse_file(sys.argv[1])
    for value in sys.argv[3:]:
        print "parse " + value
        candidates = parse_tree(value, candidates)

    with file(sys.argv[2], "w") as dest:
        with file(sys.argv[2] + ".dup", "w") as dups:
            ignored = {}
            for key, values in candidates.iteritems():
                if key not in theme:
                    ignored[key] = values
                    continue
                # copy file
                destination = path.dirname(theme[key][4])
                try:
                    makedirs(destination)
                except:
                    pass
                copy(values[0][3], destination)
                dest.write(",".join(theme[key][0:4]) + "," + " => " + ",".join(values[0][0:3]) + "," + values[0][4] + "\n")

                if len(values) > 1:
                    dups.write(",".join(theme[key][0:4]))
                    for values in values[1:]:
                        dups.write(" => " +  ",".join(values[0:3]) + "," + values[4] + "\n")
                    dups.write("\n")

    print "added:   " + str(int(((len(candidates) - len(ignored)) * 100) / len(theme))) + "% (" + str(len(candidates) - len(ignored)) + ")"
    print "ignored: " + str(int((len(ignored) * 100) / len(candidates))) + "% (" + str(len(ignored)) + ")"
    


    
    
