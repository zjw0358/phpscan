# -*- coding:UTF-8 -*- 
'''
Created on 2010-12-7

@author: spark
'''

def eval_expr(node):
#    print node
    if hasattr(node,'query'):
        result = node.query('**>Variable')
#        print [(v,v.safe) for v in result]
        unsafevars= [v for v in result if not v.safe]
        if unsafevars:
            return node
    if 'base64_decode' in str(node) or 'gzinflate' in str(node):
        return node        
#        if 'base64_decode' in str(node):
#            return node
        
queryString = '**>Eval'#eval变量
filter = eval_expr
desc = """eval a unsafe expr"""
    
    
