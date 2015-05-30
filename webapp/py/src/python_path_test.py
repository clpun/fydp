import sys
import os
import time


print "separator : " + str(os.path.abspath(os.sep))
# print the directory in which the script lives
print "script dir : " + str(os.path.abspath(os.path.realpath(__file__)))
print "running from : " + str(os.path.abspath(os.path.dirname(sys.argv[0])))
print "file : " + str(sys.argv[0])
print "current working dir : " + str(os.getcwd())