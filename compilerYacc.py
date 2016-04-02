
import ply.yacc as yacc
import compilerLex
from compilerLex import *
from compilerRDB import *

####### global function/variables ########
rdbTop = rdbProgram()
scope_stack = list()
scope_stack.append(rdbTop)
is_in_classDefn = False

def pushScope(scope):
    global scope_stack
    scope_stack.append(scope)
    #print '\n    pushing scope:', scope

def popScope():
    global scope_stack
    scope = scope_stack[len(scope_stack)-1]
    #print '    poping scope:', scope, '\n'
    scope_stack.pop()

def getScope():
    global scope_stack
    scope = scope_stack[len(scope_stack)-1]
    #print '    getting scope:',scope
    return scope

def setInClassDefn(flag):
    global is_in_classDefn
    is_in_classDefn = flag

def isInClassDefn():
    global is_in_classDefn
    return is_in_classDefn
    
def addVariable(_type, _name):
    getScope().addVar(_type, _name)

def addFunctionCall(_funcCall):
    getScope().addInstruction(_funcCall)

def addFunctionDefn(_funcDefn):
    if isInClassDefn():
        _funcDefn.setMemberFunc(True)
    getScope().addFuncDefn(_funcDefn)

def addInstruction(_expr):
    getScope().addInstruction(_expr)
    
def addClassDefn(_classDefn):
    getScope().addClassDefn(_classDefn)    

####### Top non-terminals ########        
def p_all_elements(p):
    '''all_elements : element
            | all_elements element
    '''
def p_element(p):
    '''element : include_file
            | semicolon_ended_statement
            | func_def
'''
    p[0] = p[1]

def p_semicolon_ended_statement(p):
    '''semicolon_ended_statement : vars_def end_statement
            | class_statement end_statement
            | func_call end_statement
            | assignment end_statement
'''
    p[0] = p[1]

####### Class ########
def p_class_statement(p):
    '''class_statement : class_title class_elements class_end '''
    classDefn = p[1]
    addClassDefn(classDefn)
    #print "Defined class", classDefn.getName()

def p_class_title(p):
    '''class_title : CLASS ID '{' '''
    classDefn = rdbClassDefn(p[2])
    pushScope(classDefn)
    setInClassDefn(True)
    p[0] = classDefn

def p_class_elements_iter(p):
    '''class_elements : class_elements class_element'''

def p_class_elements(p):
    '''class_elements : class_element'''
    p[0] = p[1]

def p_class_element_var(p):
    '''class_element : element'''
    p[0] = p[1]

####### Function Defn ########
def p_func_def(p):
    '''func_def : func_def_title func_def_body func_def_end'''
    funcDefn = p[1]
    addFunctionDefn(funcDefn)

def p_func_def_body_none(p):
    '''func_def_body :'''
    p[0] = None
    
def p_func_def_body_iter(p):
    '''func_def_body : func_def_body func_def_element'''
    elements = p[1]
    elements.append(p[2])
    p[0] = elements 
    
def p_func_def_body(p):
    '''func_def_body : func_def_element'''
    elements = list()
    elements.append(p[1])
    p[0] = elements
    
def p_func_def_element(p):
    '''func_def_element : element'''
    p[0] = p[1]
    
def p_func_def_title(p):
    '''func_def_title : func_def_name func_def_args ')' '{' '''
    funcDefn = p[1]
    if p[2] != None:
        for arg in p[2]:
            funcDefn.addArg(arg)
    p[0] = funcDefn
    
def p_func_def_name(p):
    '''func_def_name : type_declare ID '(' '''
    #print 'Func:', p[1], p[2]
    funcDefn = rdbFuncDefn(p[2], p[1])
    pushScope(funcDefn)
    p[0] = funcDefn

def p_func_def_args_none(p):
    'func_def_args :'
    p[0] = None
    
def p_func_def_args_iter(p):
    '''func_def_args : func_def_args ',' first_type_var_def '''
    argList = p[1]
    argList.append(p[3])
    p[0] = argList

def p_func_def_args(p):
    '''func_def_args : first_type_var_def'''
    argList = list()
    argList.append(p[1])
    p[0] = argList

def p_func_def_end(p):
    '''func_def_end : '}' '''
    popScope()

####### Function Call ########
def p_func_call(p):
    '''func_call : func_call_title func_call_args ')' '''
    funcCall = p[1]
    if p[2] != None:
        for param in p[2]:
            funcCall.addParam(param)
    addFunctionCall(funcCall)
    
def p_func_call_title(p):
    '''func_call_title : ID '(' '''
    funcName = p[1]
    #print 'Function call: ', funcName
    funcCall = rdbFuncCall(funcName)
    p[0] = funcCall

def p_func_call_title_obj(p):
    '''func_call_title : ID OBJECT_MEMBERSHIP ID '(' '''   
    funcName = p[1] + p[2] + p[3]
    #print 'Function call obj: ', funcName
    funcCall = rdbFuncCall(funcName)
    p[0] = funcCall
    
def p_func_call_title_pointer(p):
    '''func_call_title : ID POINTER_MEMBERSHIP ID '(' '''
    funcName = p[1] + p[2] + p[3]
    #print 'Function call pointer: ', funcName
    funcCall = rdbFuncCall(funcName)
    p[0] = funcCall
    
def p_func_call_args_none(p):
    '''func_call_args :'''
    p[0] = None
    
def p_func_call_args_iter(p):
    '''func_call_args : func_call_args ',' func_call_arg '''
    p[1].append(p[3])
    p[0] = p[1]
    
def p_func_call_args(p):
    '''func_call_args : func_call_arg '''
    paramList = list()
    paramList.append(p[1])
    p[0] = paramList

def p_func_call_arg_var(p):
    '''func_call_arg : ID'''
    param = rdbParam()
    param.setRefVar(p[1])
    p[0] = param

def p_func_call_arg_value(p):
    '''func_call_arg : NUMBER'''
    param = rdbParam()
    param.setValue(p[1])
    p[0] = param
    
def p_class_end(p):
    '''class_end : '}' '''
    popScope()
    setInClassDefn(False)
    
def p_end_statement(p):
    '''end_statement : ';' '''

def p_include_file(p):
    'include_file : INCLUDE include_file_name'
    p[0] = p[1]
    print p

def p_include_file_name(p):
    'include_file_name : STRING'
    p[0] = p[1]

####### Variable Defn ########
def p_vars_def(p):
    '''vars_def : vars_def ',' var_def_or_and_assignment'''
    varType = p[1]
    addVariable(varType, p[3])

def p_vars_def_first(p):
    'vars_def : first_type_var_def'
    var = p[1]
    addVariable(var.getType(), var.getName())
    p[0] = var.getType()
    
def p_first_type_var_def(p):
    'first_type_var_def : type_declare var_def_or_and_assignment'
    var = rdbVar(p[1], p[2])
    p[0] = var
    
def p_type_declare(p):
    '''type_declare : INT
                | CHAR
                | ID
    '''
    p[0] = p[1]
    
def p_var_def_or_and_assignment(p):
    '''var_def_or_and_assignment : ID
            | assignment
    '''
    p[0] = p[1]

 ####### Expression ########   
def p_assignment_number(p):
    'assignment : ID ASSIGN NUMBER'
    p[0] = p[1]
    paramL = rdbParam()
    paramL.setRefVar(p[1])
    paramR = rdbParam()
    paramR.setValue(p[3])
    expr = rdbAsignExpr(paramL, paramR)
    addInstruction(expr)

def p_assignment_expr(p):
    'assignment : ID ASSIGN expr'
    p[0] = p[1]
    paramL = rdbParam()
    paramL.setRefVar(p[1])
    paramR = rdbParam()
    paramR.setRefVar(p[3])
    expr = rdbAsignExpr(paramL, paramR)
    addInstruction(expr)

def p_expr_ID(p):
    'expr : ID'
    p[0] = p[1]

####### Yacc utils ########
def p_error(p):
    if p:
        print "Error around token: ", p, "!"
    else:
        print "Syntax error at EOF!!!!!!!"

