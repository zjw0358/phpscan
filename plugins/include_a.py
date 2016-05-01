# -*- coding:UTF-8 -*- 
'''
Created on 2010-12-8

@author: spark
'''
skip = ['DISCUZ_ROOT']
def cb_include_a(node):
#    print 'node:',node
    if hasattr(node,'expr'):
        if str(node.expr).startswith('BinaryOp'):
            if node.expr.op == '.':
                left = str(node.expr.left)
                if 'const' in left.lower():
                    return None
                right = str(node.expr.right)
                path = (left+right).lower()
#                print 'path:',path
                if '://' in path:
                    return node
                elif '.' not in right and 'php' not in path and 'inc' not in path and 'htm' not in path:
                    return node

queryString = '**>Include'
filter = cb_include_a
desc = """include a dange file  """