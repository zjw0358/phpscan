# -*- coding:UTF-8 -*- 
'''
Created on 2010-12-8

@author: spark
'''

def cb_require_b(node):
    if hasattr(node,'expr'):
        if str(node.expr).startswith('BinaryOp'):
            if node.expr.op == '.':
                left = str(node.expr.left)
                right = str(node.expr.right)
                path = (left+right).lower()
#                print 'path:',path
                if '://' in path:
                    return node
                elif '.' not in right and 'php' not in path and 'inc' not in path and 'htm' not in path:
                    return node

queryString = '**>Require'
filter = cb_require_b
desc = """require a dange file """