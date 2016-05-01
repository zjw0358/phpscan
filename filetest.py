'''
Created on 2010-11-29

@author: spark
'''
from phpar import phplex
from phpar.phpparse import parser
from phpar.phpast import *

import pprint
import message

def visitor(node):
    if hasattr(node,'parent'):
        print 'parent:',node.parent
    if isinstance(node,FunctionCall):
        if hasattr(node,'name'):
#        if node.name in dangefuncs:
            print 'line %s,func call:%s,parames:%s,type:%s' %(node.lineno,node.name,node.params,node.type)
        else:
            print node
    if isinstance(node,Eval):
        print 'line %s,eval:%s,type:%s' %(node.lineno,node.expr,node.type)
    if isinstance(node,Variable):
        print node.name      
            
dangevars = ['$_GET']
def dangeit(node):
    print 'dange node:%s'%(node.name)
    node.safe=False
    dangevars.append(node.name)

if __name__ == '__main__':
    lexer = phplex.lexer.clone()
    lexer.filename = None
    input = file(r'D:\office\test6.php','r').read()
    output = parser.parse(input, lexer=lexer)
#    to_graph(output[0],'testyacc')
    if output:
        for item in output:                               
            if hasattr(item,'query'):
                result =  item.query('**>Eval')#Variable
                if result:
                    for r in result:
                        print r


##                print item
#                to_graph(item,'testyacc'+str(item)[:3])
#                print item.fields
#                item = item.generic(with_lineno=True)

#            if hasattr(item,'generic'):
#                pprint.pprint(item.generic())
#                print '-'*8
##                
#            if hasattr(item,'accept'):
#                item.accept(visitor)


