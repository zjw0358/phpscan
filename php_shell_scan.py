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
from phpar.phpast import *
import pprint
import sys
import os
import message

USAGE = """
---------------------------------------------------
   php_shell_scan.exe - a program to scan directories
       for possible php shell infections.
       Copyright (c) 2010, SparkZhang
             spark@secsay.com
-----------------------USAGE-----------------------
TARGET : directory or filename

exsample:
>>> php_shell_scan.exe TARGET 
OR
>>>php_shell_scan.exe TARGET maybe

""" 
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class Log():
    count = 0
    log = []
    result = {}
    logline = 0
    def __init__(self):
        self.log.append('log begin')
    def message(self,message):
        print (bcolors.WARNING+message+' '*(strlen-len(message))+bcolors.ENDC)
        # print message+' '*(strlen-len(message))
        self.log.append(message)
        scanlog.write(message+'\n')
    def add_result(self,url,forms):
        self.result[url]= forms
        #print 'result:%s forms find in %s' % (len(forms),url)
#        file('log.log','a').write('url:%s\n forms:%s\n' % (url,'\n'.join([f.toString() for f in forms])))
                                  
class Plus():
    def __init__(self,name,plugin):
        try:
            self.log = Log()
            self.name = name
            self.result = []
            self.qs = plugin.queryString
            self.filter = plugin.filter
            self.desc = plugin.desc
            self.log.message('install plugins %s success'%name) 
            self.log.message( '-'*80)
        except:
            self.log.message('install plugins %s error'%name)
class Analizer():
    def __init__(self):
        self.lexer = phplex.lexer.clone()
        self.lexer.filename = None 
        self.log = Log()   
        self.dangevars = ['$_GET']
#        self.plugins = Plus()     
    def dangeit(self,var):
#        print 'dange var:%s'%(var.name)
        var.safe=False
        self.dangevars.append(var.name)
    def varcheck(self,item):
        if hasattr(item,'query'):
            vars =  item.query('**>Variable')
            for v in vars:
                if v.name in self.dangevars:
                    v.safe = False
                if '$_' in str(v.name):
                    self.dangeit(v)
                        
            ass =  item.query('**>Assignment')#Variable
            for a in ass:
                if isinstance(a.node,Variable):
                    if not a.node.safe:
                        self.dangeit(a.node)
                    if hasattr(a.expr,'query'):
                        vs = a.expr.query('**>Variable')
                        for v in vs:
                            if not v.safe:
                                self.dangeit(a.node)               
    def analysis(self,filename):
        self.filename = filename
        f = open(filename)
        self.input = f.read()
        f.close()
        output = parser.parse(self.input, lexer=self.lexer)
        result = []
        if output:
            for item in output:
                try:
                    self.varcheck(item)#影响后面的插件
                except:
                    print 'var safe check fail'
                if hasattr(item,'query'):
                    for plus in p:
                        try:
                            plus.result = item.query(plus.qs,plus.filter) 
                            if plus.result:
    #                            print 'result:',plus.result
                                for n in set(plus.result):
                                    self.log.message('      %s desc:%s'%
                                                     (plus.name,plus.desc,
                                                       ))
                                    self.log.message('  -->Code:%s line:%s'%
                                                     (self.input.split('\n')[n.lineno-1].strip()[:100],
                                                       n.lineno))
                                    result.append(plus.result)
                        except:
                            pass
#                            self.log.message('%s error when process %s'%(plus.name,filename))
        
        return result
    

                  
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
            analizer = Analizer()
            if analizer.analysis(fname):
#                sys.stdout.write(' '*strlen)  
                log.message( 'File:%s\n' %fname)
                log.message( '-'*80)
    except: pass
    vcount += 1 
    
def scaner(args, directoryName,filesInDirectory):     # called for each dir 
    for fname in filesInDirectory:                   
        fpath = os.path.join(directoryName, fname)    
        if not os.path.isdir(fpath):                    
            scanfile(fpath,args)
    
def scan(startdir):
    
    global leval
    global fcount, vcount
    fcount = vcount = 0
    install_plugins(leval=leval)
    if os.path.isfile(startdir):
        scanfile(startdir,'') 
    else:
        os.path.walk(startdir, scaner, '')
        print "scan finished"+' '*(strlen-13) 
     
def install_plugins(leval):
    try:
        import plugins
        print 'Loading plugins'
    except:
        print 'install plugins error'
        sys.exit()
    if leval == 0:
        pns = [pn for pn in plugins.plugins if pn[-1]=='a']
        for pn in pns:
            p.append(Plus(pn,plugins.plugins[pn]))
    if leval == 1:
        pns = [pn for pn in plugins.plugins if pn[-1]=='b']
        for pn in pns:
            p.append(Plus(pn,plugins.plugins[pn]))
    
skipexts = ['.gif', '.exe', '.pyc', '.o', '.a','.dll','.lib','.pdb','.mdb']        # ignore binary files
scanexts = ['.inc','.php','.py','.html'] 
strlen = 0 
log = Log()
p = []
leval = 0
scanlog = open('scan.log','a+')
if __name__ == '__main__':
    
    if os.name =='nt':
        os.system('color 0a')
        os.system('mode con cols=155 lines=300')
    args = sys.argv
    if len(args) == 2:
    	from phpar.phpparse import parser
        scan(args[1])
    elif len(args) == 3:
    	from phpar.phpparse import parser
        leval = 1
        scan(args[1])
    else:
        print USAGE
