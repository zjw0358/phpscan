# -*- coding:UTF-8 -*- 
'''
Created on 2010-12-7

@author: spark
'''

dangefuncs = ['assert','proc_open','popen','shell_exec','exec','passthru','system',
                  'import_request_variables',
                  'create_function','get_defined_vars',
                  'fputs','fopen',]
otherfuncs = ['array_map','explode','print_r',]
def cb_func_a(node):
#    print node
    if node.name in dangefuncs:
        for param in node.parames:
            print 'parm:',param
            if hasattr(param,'query'):
                result = param.query('**>Variable')
                safe = True
                for v in result:
                    if  hasattr(v,'safe') and not v.safe:
                        safe = False
                if not safe:
                    return node
            
    if hasattr(node.name,'query'):
        result = node.name.query('**>Variable')
        for v in result:
            if not v.safe:
                return node
            
        
                  
queryString = r'**>FunctionCall'
filter = cb_func_a 
desc = """userinput func name or dange func with dange var params"""


        


        