#! /usr/bin/env python

import sys, os, os.path
import pyctf

__usage = """[-c color] mark file dataset
Add the marks in file to the dataset using the name 'mark'. The file must
contain lines of the form 'trial time'; trial starts at 0 and time is in
seconds. The color defaults to 'blue'."""

__scriptname = os.path.basename(sys.argv[0])

def printerror(s):
    sys.stderr.write("%s: %s\n" % (__scriptname, s))
msg = printerror

def printusage():
    sys.stderr.write("usage: %s %s\n" % (__scriptname, __usage))

color = 'blue'
argv = sys.argv[1:]

if len(argv) > 1 and argv[0] == '-c':
    color = argv[1]
    argv = argv[2:]

if len(argv) != 3:
    printusage()
    sys.exit(1)

marker = argv[0]
fname = argv[1]
dsname = argv[2]

# Open the dataset.

ds = pyctf.dsopen(dsname)

ntr = ds.getNumberOfTrials()
nsamp = ds.getNumberOfSamples()
srate = ds.getSampleRate()
pretrig = ds.getPreTrig()
marks = ds.marks.keys()

dur = nsamp / srate
x = pretrig
if x != 0.:
    x = -x
start = x
end = start + dur

# Read the new marks.

try:
    f = open(fname)
except:
    printerror("Can't read file '{}'".format(fname))
    sys.exit(1)

m = []
for l in f:
    l = l.strip()
    s = l.split()
    if len(s) != 2:
        printerror("Improperly formatted line '{}' in '{}'".format(l, fname))
        sys.exit(1)
    tr = int(s[0])
    t = float(s[1])
    if tr < 0 or tr+1 > ntr:
        printerror("Bad trial number, line '{}' in '{}'".format(l, fname))
        printerror("Trial must be less than {}".format(ntr))
        sys.exit(1)
    if t < start or t > end:
        printerror("Bad time, line '{}' in '{}'".format(l, fname))
        printerror("Time must be in the range [{:g}, {:g}]".format(start, end))
        sys.exit(1)
    m.append((tr, t))

# Add/replace the mark.

s = "Adding"
if ds.marks.get(marker) is not None:
    s = "Replacing"
    marks = [mark for mark in marks if mark != marker]
msg("{} mark '{}' in {}.".format(s, marker, dsname))

# Delete the old MarkerFile.mrk, and recreate it.

mrk = ds.getDsFileName("MarkerFile.mrk")
os.system("rm -f {}".format(mrk))
f = open(mrk, "w")

classid = 0
def writeMark(mark, m, f):
    global classid

    classid += 1
    f.write("CLASSGROUPID:\n3\n")
    f.write("NAME:\n{}\n".format(mark))
    f.write("COMMENT:\n(PositionFile={})\n".format(fname))
    f.write("COLOR:\n{}\n".format(color))
    f.write("EDITABLE:\nYes\n")
    f.write("CLASSID:\n{}\n".format(classid))
    f.write("NUMBER OF SAMPLES:\n{}\n".format(len(m)))
    f.write("LIST OF SAMPLES:\n")
    f.write("TRIAL NUMBER\t\tTIME FROM SYNC POINT (in seconds)\n")
    for tr, t in m:
        f.write("{:20d}{:+48.12g}\n".format(tr, t))
    f.write("\n\n")

f.write("PATH OF DATASET:\n{}\n\n\n".format(ds.dsname))
f.write("NUMBER OF MARKERS:\n{}\n\n\n".format(len(marks) + 1))

# Copy the old ones
for mark in marks:
    writeMark(mark, ds.marks[mark], f)

# Now the new one
writeMark(marker, m, f)
