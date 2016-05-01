########################################## INFO ##########################################
#
# Name:          php_shell_scan.py
# Version:       0.0.3
# Author:        SparkZhang
# Contact:       zjw0358 AT gmail.com
# Last Updated:  2010-11-2
#
# A script to scan a a web server's directories for the presence of a PHP shell.
# 

USAGE = """
---------------------------------------------------
   php_shell_scan.py - a script to scan directories
       for possible php shell infections.
       Copyright (c) 2010, SparkZhang
-----------------------USAGE-----------------------

topdir  - The top level directory you wish to scan.
          All subdirectories and files will scanned
logfile - file to write results to. Will be written
          to cwd if not specified.

>>>php_shell_scan_re.exe topdir


"""




import sys
import os
import re

def check(file):
    i = 0
    iname = 0
    f = open(file)
    while f:
        file_contents = f.readline()
        if not file_contents:
            break
        i += 1
        match = re.search(r'''(?P<function>\b(?:include|require)(?:_once)?\b)\s*\(?\s*["'](?P<filename>[^;]*(?<!\.(?:php|inc)))["']\)?\s*;''', file_contents, re.IGNORECASE| re.MULTILINE)
        if match:
            function = match.group("function")
            filename = match.group("filename")
            if iname == 0:
                info = '\n[%s] :\n'% (file)
            else:
                info = ''
            info += '\t|-- [%s] - [%s]  line [%d] \n'% (function,filename,i)
            info += '\t\tcode:%s\n' % file_contents.strip()[:100]
            flog.write(info)
            print info
            iname += 1
        match = re.search(r'\b(?P<function>eval|proc_open|popen|shell_exec|exec|passthru|system)\b\s*\(', file_contents, re.IGNORECASE| re.MULTILINE)
        if match:
            function = match.group("function")
            if iname == 0:
                info = '\n[%s] :\n'% (file)
            else:
                info = ''
            info += '\t|-- [%s]  line [%d] \n'% (function,i)
            info += '\t\tcode:%s\n' % file_contents.strip()[:100]
            flog.write(info)
            print info
            iname += 1
        match = re.search(r'(^|(?<=;))\s*`(?P<shell>[^`]+)`\s*;', file_contents, re.IGNORECASE)
        if match:
            shell = match.group("shell")
            if iname == 0:
                info = '\n[%s] :\n'% (file)
            else:
                info = ''
            info += '\t|-- [``] command is [%s] in line [%d] \n'% (shell,i)
            info += '\t\tcode:%s\n' % file_contents.strip()[:100]
            flog.write(info)
            print info
            iname += 1
    f.close()

def scanfile(fname, searchKey):                       # for each non-dir file
    global fcount, vcount                              
    try:
        if not listonly:
            
            if os.path.splitext(fname)[1].lower() in skipexts:
                pass
            #if re.search(r"\.(?:php|inc?)$", os.path.basename(fname), re.IGNORECASE):
            elif os.path.splitext(fname)[1].lower() in scanexts :
                check(fname)
    except: pass
    vcount += 1 
    
def scaner(args, directoryName,filesInDirectory):     # called for each dir 
    for fname in filesInDirectory:                   
        fpath = os.path.join(directoryName, fname)    
        if not os.path.isdir(fpath):                   
            scanfile(fpath,args)
     
def scan(startdir):
    global fcount, vcount
    fcount = vcount = 0
    os.path.walk(startdir, scaner,'')
     

flog = open('relog.log','a+')
listonly = False
skipexts = ['.gif', '.exe', '.pyc', '.o', '.a','.dll','.lib','.pdb','.mdb']        # ignore binary files
scanexts = ['.inc','.php']     

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        print USAGE
        os.system("cmd.exe")
    elif len(args) == 2:
        scan(args[1])
    elif len(args) == 3:
        scan(args[1])
    else:
        print USAGE
