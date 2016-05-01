# -*- coding:UTF-8 -*- 
# ----------------------------------------------------------------------
# phpast.py
#
# PHP abstract syntax node definitions.
# ----------------------------------------------------------------------

class Node(object):
#    children = []
#    fields = []
    queryret = []
    def __init__(self, *args, **kwargs):
        assert len(self.children) == len(args), \
            '%s takes %d arguments' % (self.__class__.__name__,
                                       len(self.children))

        try:
            self.lineno = kwargs['lineno']
        except KeyError:
            self.lineno = None
        self.type = self.__class__.__name__   
        for i, child in enumerate(self.children):
            setattr(self, child, args[i])    
        self._attr = {}
        self.safe = True
        self.parent = None
        self.fields=self.children
#        for child in self.children:
#            if isinstance(child,Node):
#                print type(child),child
#                child.parent = self
        for field in self.fields:
            child = getattr(self, field)
            if isinstance(child,Node):
                child.parent = self
            if isinstance(child,list):
                for i in child:
                    if isinstance(i,Node):
                        i.parent = self
            if isinstance(child,str):
                pass
                
#                print 'parent,',child.parent      
        


    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__,
                           ', '.join([repr(getattr(self, child))
                                      for child in self.children]))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for child in self.children:
            if not (getattr(self, child) == getattr(other, child)):
                return False
        return True

    def accept(self, visitor):
        visitor(self)
        for child in self.children:
            value = child#getattr(self, child)
            if isinstance(value, Node):
                value.accept(visitor)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, Node):
                        item.accept(visitor)

    def generic(self, with_lineno=False):
        values = {}
        if with_lineno:
            values['lineno'] = self.lineno
        for field in self.fields:
            value = getattr(self, field)
            if hasattr(value, 'generic'):
                value = value.generic(with_lineno)
            elif isinstance(value, list):
                items = value
                value = []
                for item in items:
                    if hasattr(item, 'generic'):
                        item = item.generic(with_lineno)
                    value.append(item)
            values[field] = value
        return (self.__class__.__name__, values)

    def getChildren(self):
        return self.children

    def __iter__(self):
        for n in self.children:
            yield n

    def __getitem__(self, ind):
        return self.children[ind]

#    def __getattr__(self, attr):
#        #create Getter and Setter methods for node attribute
#        if attr.startswith("set_"):
#            attr_name = attr.split('_')[1]
#            t = lambda x, a=attr_name : self._attr.__setitem__(a, x)
#            self.__setattr__(attr,  t)
#            return t
#        elif attr.startswith("get_"):
#            attr_name = attr.split('_')[1]
#            t = lambda a=attr_name : self._attr.__getitem__(a)
#            self.__setattr__(attr,  t)
#            return t

    def __len__(self):
        return len(self.children)

    def child(self, q):
        if isinstance(q, int):
            return self.children[q]
        elif isinstance(q, str):
            result = self.query(q)
            if len(result) == 1:
                return result[0]

    def ancestor(self, type):
        p = self.parent
        while(p):
            if p.type == type:
                break
            else:
                p = p.parent
        return p

    def prev_all(self, node_type):
        siblings  = self.parent.getChildren()
        ret = []
        for sibling in siblings:
            if sibling is self:
                break
            elif sibling.type == node_type:
                ret.append(sibling)
        return ret

    def prev(self, type):
        r = self.prev_all(type)
        if len(r) >= 1:
            return r[0]
        else:
            return None
    def filter(self,node):
        return node

    def query(self,q="*",filter=None):
        '''查询的语法如下 [type|*] {>[type|*]}
        eg.  fdef  类型为fdef 的子结点
             fdef>vdecl 类型为fdef的子结点下面的类型为vdecl的子结点
             *>exp 第二层的exp结点
             **>exp 所有类型为exp 的结点。（不管层次)
             ××>?所有叶结点
             ? 表示叶结点
        '''
        if filter == None:
            filter=self.filter
        else:
            filter = filter
        ret = []
        qs = q.split(">")
        if self.is_type_match(qs[0]) or qs[0] == '*' :
#            r = apply(filter,(self,))
            ret.append(self) 
#            print 'append',self
        if qs[0] =='**' and self.is_type_match(qs[1]):
            ret.append(self) 
        
        for field in self.fields:
            child = getattr(self, field)
            if child is None:
                continue
            if isinstance(child, list):
                for i in child :
                    if isinstance(i,Node):
                        ret.extend(i.query(q,filter=filter))

#                continue
            if not isinstance(child,Node):
                continue
            if child.is_type_match(qs[0]) or qs[0] == '*':
                if len(qs) > 1:
                    ret.extend(child.query(">".join(qs[1:]),filter=filter))
                else:
#                    child = apply(filter,(child,))
                    ret.append(child)                   
#                    print 'append',child
            elif qs[0] == '**':
                if len(qs) == 2:
#                    if child.is_type_match(qs[1]):
#                        ret.append(child)    
                    ret.extend(child.query(q,filter=filter))
                    
        ret = [apply(filter,(r,)) for r in ret if isinstance(r,Node)]
        ret = [r for r in ret if r!=None]
        return ret

    def is_type_match(self, type):
        #TODO ? is no longer work , as we do have a ? type
        if self.fields == ['name'] and type == '?':
            return True
        if self.type == type:
            return True
        return False


    def set_attr(self, name, value):
        self._attr[name] = value


    def get_attr(self, name):
        r =  self._attr.get(name, None)
        #if r is None:
            #print "get %s from Node %s  got None" %(name , self)
        return r


    def get_postion(self):
        lextokens = self.query("**>?")
        return (lextokens[0].lineno, lextokens[-1].lineno)
#    def __repr__(self):
#        #return "<Node type=%s [%s]>" %(self.type, str(self.children))
#        return " ".join([repr(x) for x in self.query("**>?")])

    __str__ = __repr__


def node(name, children):
    attrs = {'children': children}
    return type(name, (Node,), attrs)

InlineHTML = node('InlineHTML', ['data'])
Block = node('Block', ['nodes'])
Assignment = node('Assignment', ['node', 'expr', 'is_ref'])
ListAssignment = node('ListAssignment', ['nodes', 'expr'])
New = node('New', ['name', 'params'])
Clone = node('Clone', ['node'])
Break = node('Break', ['node'])
Continue = node('Continue', ['node'])
Return = node('Return', ['node'])
Global = node('Global', ['nodes'])
Static = node('Static', ['nodes'])
Echo = node('Echo', ['nodes'])
Print = node('Print', ['node'])
Unset = node('Unset', ['nodes'])
Try = node('Try', ['nodes', 'catches'])
Catch = node('Catch', ['class_', 'var', 'nodes'])
Throw = node('Throw', ['node'])
Declare = node('Declare', ['directives', 'node'])
Directive = node('Directive', ['name', 'node'])
Function = node('Function', ['name', 'params', 'nodes', 'is_ref'])
Method = node('Method', ['name', 'modifiers', 'params', 'nodes', 'is_ref'])
Closure = node('Closure', ['params', 'vars', 'nodes', 'is_ref'])
Class = node('Class', ['name', 'type', 'extends', 'implements', 'nodes'])
ClassConstants = node('ClassConstants', ['nodes'])
ClassConstant = node('ClassConstant', ['name', 'initial'])
ClassVariables = node('ClassVariables', ['modifiers', 'nodes'])
ClassVariable = node('ClassVariable', ['name', 'initial'])
Interface = node('Interface', ['name', 'extends', 'nodes'])
AssignOp = node('AssignOp', ['op', 'left', 'right'])
BinaryOp = node('BinaryOp', ['op', 'left', 'right'])
UnaryOp = node('UnaryOp', ['op', 'expr'])
TernaryOp = node('TernaryOp', ['expr', 'iftrue', 'iffalse'])
PreIncDecOp = node('PreIncDecOp', ['op', 'expr'])
PostIncDecOp = node('PostIncDecOp', ['op', 'expr'])
Cast = node('Cast', ['type', 'expr'])
IsSet = node('IsSet', ['nodes'])
Empty = node('Empty', ['expr'])
Eval = node('Eval', ['expr'])
Include = node('Include', ['expr', 'once'])
Require = node('Require', ['expr', 'once'])
Exit = node('Exit', ['expr'])
Silence = node('Silence', ['expr'])
MagicConstant = node('MagicConstant', ['name', 'value'])
Constant = node('Constant', ['name'])
Variable = node('Variable', ['name'])
StaticVariable = node('StaticVariable', ['name', 'initial'])
LexicalVariable = node('LexicalVariable', ['name', 'is_ref'])
FormalParameter = node('FormalParameter', ['name', 'default', 'is_ref'])
Parameter = node('Parameter', ['node', 'is_ref'])
FunctionCall = node('FunctionCall', ['name', 'params'])
Array = node('Array', ['nodes'])
ArrayElement = node('ArrayElement', ['key', 'value', 'is_ref'])
ArrayOffset = node('ArrayOffset', ['node', 'expr'])
StringOffset = node('StringOffset', ['node', 'expr'])
ObjectProperty = node('ObjectProperty', ['node', 'name'])
StaticProperty = node('StaticProperty', ['node', 'name'])
MethodCall = node('MethodCall', ['node', 'name', 'params'])
StaticMethodCall = node('StaticMethodCall', ['class_', 'name', 'params'])
If = node('If', ['expr', 'node', 'elseifs', 'else_'])
ElseIf = node('ElseIf', ['expr', 'node'])
Else = node('Else', ['node'])
While = node('While', ['expr', 'node'])
DoWhile = node('DoWhile', ['node', 'expr'])
For = node('For', ['start', 'test', 'count', 'node'])
Foreach = node('Foreach', ['expr', 'keyvar', 'valvar', 'node'])
ForeachVariable = node('ForeachVariable', ['name', 'is_ref'])
Switch = node('Switch', ['expr', 'nodes'])
Case = node('Case', ['expr', 'nodes'])
Default = node('Default', ['nodes'])
Namespace = node('Namespace', ['name', 'nodes'])
UseDeclarations = node('UseDeclarations', ['nodes'])
UseDeclaration = node('UseDeclaration', ['name', 'alias'])
ConstantDeclarations = node('ConstantDeclarations', ['nodes'])
ConstantDeclaration = node('ConstantDeclaration', ['name', 'initial'])

#class Leaf(Node):
#
#    def __init__(self, type, value):#, lineno, lexpos):
#        self.type = type
#        self.value = value
##        self.lineno = lineno
##        self.lexpos = lexpos
#        self.children = []
#        self._attr = {}
#        self.set_attr('value', self.value)
#
#    def __len__(self):
#        return 0
#
#    def query(self,qs):
#        return []
#
#    def __repr__(self):
#        return str(self.value)
#        #return str("<Leaf : %s>" %(self.value,))
#
#    __str__ = __repr__
def resolve_magic_constants(nodes):
    current = {}
    def visitor(node):
        if isinstance(node, Namespace):
            current['namespace'] = node.name
        elif isinstance(node, Class):
            current['class'] = node.name
        elif isinstance(node, Function):
            current['function'] = node.name
        elif isinstance(node, Method):
            current['method'] = node.name
        elif isinstance(node, MagicConstant):
            if node.name == '__NAMESPACE__':
                node.value = current.get('namespace')
            elif node.name == '__CLASS__':
                node.value = current.get('class')
                if current.get('namespace'):
                    node.value = '%s\\%s' % (current.get('namespace'),
                                             node.value)
            elif node.name == '__FUNCTION__':
                node.value = current.get('function')
                if current.get('namespace'):
                    node.value = '%s\\%s' % (current.get('namespace'),
                                             node.value)
            elif node.name == '__METHOD__':
                node.value = current.get('method')
                if current.get('class'):
                    node.value = '%s::%s' % (current.get('class'),
                                             node.value)
                if current.get('namespace'):
                    node.value = '%s\\%s' % (current.get('namespace'),
                                             node.value)
    for node in nodes:
        if isinstance(node, Node):
            node.accept(visitor)


#导出成图片
#using pydot and graphviz
try:
    import pydot
    def node_to_graph(node, graph):
        if not isinstance(node,Node):# is None or type(node)==type('str'):
            return None
        parent = pydot.Node(
            id(node)
        )
        if hasattr(node,'name'):
            parent.set_label(node.__class__.__name__+'->'+str(node.name))
        else:
            parent.set_label(node.__class__.__name__+'->'+str(node))
        graph.add_node(parent)
        #print parent.to_string()
        if hasattr(node,'children'):
            for n in node.children:
                child = node_to_graph(getattr(node,n), graph)
                print 'a :',getattr(node,n)
                if child:
                    graph.add_edge(pydot.Edge(parent, child))
            return parent

    def to_graph(root, graph_name):
        graph = pydot.Dot()
        node_to_graph(root, graph)
        print graph.to_string()
        graph.write_png(graph_name + '.png', prog='dot')

except ImportError:
    def to_graph(root, graph_name):
        print "pydot is not installed.to_graphp will not work"