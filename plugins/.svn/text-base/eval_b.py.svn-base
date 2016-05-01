# -*- coding:UTF-8 -*- 
'''
Created on 2010-12-7

@author: spark
'''
def cb_eval_b(node):#误报较多，为了查杀大马，需要加新的特征
#    if 'post' in str(node) or 'get' in str(node).lower():
    if isinstance(node.expr,str) and 'Variable' in str(node):
        return node
    if hasattr(node,'query') and node.query('**>Variable'):
        return node
    if '$_' in str(node):
        return node
    
    
queryString = '**>Eval'
filter = cb_eval_b 
desc = """eval a expr"""