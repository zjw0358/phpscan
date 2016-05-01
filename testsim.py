# -*- coding:UTF-8 -*- 
#
# Name:          php_shell_scan.py
# Version:       0.0.3
# Author:        SparkZhang
# Contact:       zjw0358 AT gmail.com
# Last Updated:  2010-11-2
#
# A script to scan a a web server's directories for the presence of a PHP shell.
# 
from phpar import phplex
from phpar.phpparse import parser
from phpar.phpast import *
import sys
import os
import message
class Log():
    count = 0
    log = []
    result = {}
    logline = 0
    def __init__(self):
        self.log.append('log begin')
    def message(self,message):
#        print (bcolors.WARNING+message+' '*(strlen-len(message))+bcolors.ENDC)
        print message+' '*(strlen-len(message))
        self.log.append(message)
    def add_result(self,url,forms):
        self.result[url]= forms
                          
def scanfile(fname, searchKey):                       # for each non-dir file
    global fcount, vcount ,strlen                             
    try:

        if os.path.splitext(fname)[1].lower() in skipexts:
            pass
        #if re.search(r"\.(?:php|inc?)$", os.path.basename(fname), re.IGNORECASE):
        elif os.path.splitext(fname)[1].lower() in scanexts :
            progressStr = 'Scanning %s' %(fname,)
            if len(progressStr)>strlen:
                strlen = len(progressStr)
            else:
                progressStr = progressStr+' '*(strlen-len(progressStr))
            sys.stdout.write(progressStr)
            sys.stdout.flush()
            sys.stdout.write('\b'*strlen)  
            sys.stdout.flush()
            if os.name =='nt':
                os.system('title '+progressStr)
            
            s2 = file(fname).read()
            hash2 = simhash.simhash(getvarlist(s2))
            log.message( "%s is percent similar %s"%(hash1.similarity(hash2),fname))



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

    if os.path.isfile(startdir):
        scanfile(startdir,'') 
    else:
        os.path.walk(startdir, scaner, '')
        print "scan finished"+' '*(strlen-13) 
     
def getvarlist(input):
    output= parser.parse(input, lexer=lexer)
    varst = ''
    for item in output:                               
        if hasattr(item,'query'):
            result =  item.query('**>Variable')#Variable
            if result:
                for r in result:
                    varst += str(r.name)
                     
    return varst
    
skipexts = ['.gif', '.exe', '.pyc', '.o', '.a','.dll','.lib','.pdb','.mdb']        # ignore binary files
scanexts = ['.inc','.php'] 
strlen = 0 
lexer = phplex.lexer.clone()
lexer.filename = None

p = []
s1 = file('d:\\office\\2008.php').read()
log = Log()
import simhash
hash1 =simhash.simhash(getvarlist(s1))
if __name__ == '__main__':
    
    if os.name =='nt':
        os.system('color 0a')
        os.system('mode con cols=155 lines=300')
    args = sys.argv
    if len(args) == 2:
        scan(args[1])
    elif len(args) == 3:
        scan( args[2])
    elif len(args) == 4:
        scan(args[2])
    else:
        pass
