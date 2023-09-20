#! /usr/bin/env python

import sys, os, os.path
import tempfile
import pyctf

__usage = """mark dataset
Delete the named marker from the dataset."""

__scriptname = os.path.basename(sys.argv[0])

def printerror(s):
    sys.stderr.write("%s: %s\n" % (__scriptname, s))

def printusage():
    sys.stderr.write("usage: %s %s\n" % (__scriptname, __usage))

if len(sys.argv) != 3:
    printusage()
    sys.exit(1)

marker = sys.argv[1]
dsname = sys.argv[2]

ds = pyctf.dsopen(dsname)

if ds.marks.get(marker) is None:
    printerror("No such mark {} in {}.".format(marker, dsname))
    sys.exit(1)

goodmarks = [mark for mark in ds.marks.keys() if mark != marker]

# First, extract all the good marks from the dataset, and write them
# to temporary files.

TempDir = tempfile.mkdtemp()
assert len(TempDir) != 0

def cleanup(normal = False):
    os.system("rm -rf {}".format(TempDir))
    if not normal:
        sys.exit(1)
    sys.exit(0)

d = {}
try:
    for mark in goodmarks:

        # Create a unique filename for the mark.

        fd, name = tempfile.mkstemp(dir = TempDir, text = True)
        f = os.fdopen(fd, 'w')
        d[mark] = name

        # Write it out.

        for tr, t in ds.marks[mark]:
            f.write("{} {}\n".format(tr, t))

        f.close()
except Exception as msg:
    printerror(msg)
    cleanup()

# Now delete the old MarkerFile.mrk, and recreate it.

mrk = ds.getDsFileName("MarkerFile.mrk")
os.system("rm -f {}".format(mrk))

if len(goodmarks) == 0:
    cleanup(True)

print("Remaining marks:")
for mark in goodmarks:
    print(mark)
    os.system("addMarker.py '{}' {} {}".format(mark, d[mark], dsname))

cleanup(True)
