
from util import *

############################
class rdbParam:
    def __init__(self):
        self.valueType = 'Value'
        self.refVar = None
        self.value = None

    def setValue(self, value):
        self.value = value
        self.valueType = 'Value'

    def getValue(self):
        return self.value

    def setRefVar(self, var):
        self.refVar = var
        self.valueType = 'RefVar'

    def getRefVar(self):
        return self.refVar

    def isRefValue(self):
        return (self.valueType == 'RefVar')

    def valueToStr(self):
        paramValue = ''
        if self.isRefValue():
            paramValue = self.getRefVar()
        else:
            paramValue = str(self.getValue())
        return paramValue

#######################
class rdbFuncCall:
    def __init__(self, name):
        self.name = name
        self.params = list()
        self.paramCount = 0

    def getName(self):
        return self.name
    
    def addParam(self, param):
        self.params.append(param)
        self.paramCount += 1

    def getParamCount(self):
        return self.paramCount

    def getParam(self, i):
        if i < self.paramCount:
            return self.params[i]
        else:
            return None

    def dump(self, level):
        offset = getDumpOffset(level)
        paramsStr = ''
        for i in range(self.paramCount):
            param = self.params[i]
            paramValue = param.valueToStr()
            paramsStr += paramValue
            if i < (self.paramCount-1):
                paramsStr += ","
        print offset + 'calling function: %s(%s)' % (self.name,paramsStr)

#######################
class rdbAsignExpr:
    def __init__(self, paramL, paramR):
        self.paramL = paramL
        self.paramR = paramR

    def getParamL(self):
        return self.paramL

    def getParamR(self):
        return self.paramR

    def dump(self, level):
        offset = getDumpOffset(level)
        print offset + 'excute: %s = %s' % (self.paramL.getRefVar(), self.paramR.valueToStr())
        
#######################
class rdbExpr:
    def __init__(self, expr):
        self.expr = expr


#######################
class rdbVar:
    def __init__(self, varType, varName):
        self.varType = varType
        self.varName = varName

    def getName(self):
        return self.varName

    def getType(self):
        return self.varType

#######################
class rdbContext:
    def __init__(self):
        self.vars = list()
        self.instructions = list()
        self.funcDefns = list()
        self.classDefns = list()
        #TODO: use set to find duplicated defns. need to check the overload func

    def addVar(self, varName, varType):
        var = rdbVar(varName, varType);
        self.vars.append(var)

    def getVars(self):
        return self.vars
        
    def addInstruction(self, instruction):
        self.instructions.append(instruction)

    def getInstructions(self):
        return self.instructions
    
    def addFuncDefn(self, funcDefn):
        self.funcDefns.append(funcDefn)

    def getFuncDefns(self):
        return self.funcDefns

    def addClassDefn(self, classDefn):
        self.classDefns.append(classDefn)

    def getClassDefns(self):
        return self.classDefns

    def dump(self, level):
        offset = getDumpOffset(level-1)
        print offset + '{'
        offset = getDumpOffset(level)
        offsetContent = getDumpOffset(level+1)
        if len(self.classDefns) != 0:
            print offset+'classDefns:'
            for i in self.classDefns:
                i.dump(level+1);
        if len(self.funcDefns) != 0:
            print offset+'funcDefns:'
            for i in self.funcDefns:
                i.dump(level+1);
        if len(self.vars) != 0:
            print offset+'vars:'
            for i in self.vars:
                print offsetContent + 'name=%s type=%s' % (i.getName(), i.getType())
        if len(self.instructions) != 0:
            print offset+'instructions:'
            for i in self.instructions:
                i.dump(level+1);
        offset = getDumpOffset(level-1)
        print offset + '}\n'
                        

#######################
class rdbNamedContext(rdbContext):
    def __init__(self, name):
        rdbContext.__init__(self)
        self.name = name

    def dump(self, level):
        #print 'level: %d' %level
        offset = getDumpOffset(level)
        print offset + self.name
        rdbContext.dump(self, level+1)       
        
#######################
class rdbFuncDefn(rdbNamedContext):
    def __init__(self, name, retType):
        rdbNamedContext.__init__(self, name)
        self.retType = retType
        self.isMemFunc = False
        self.argv = list()
        self.argc = 0

    def getName(self):
        return self.name

    def getRetType(self):
        return self.retType

    def setMemberFunc(self, isMemFunc):
        self.isMemFunc = isMemFunc
        
    def isMemberFunc(self):
        return self.isMemFunc
    
    def addArg(self, arg):
        self.argv.append(arg)
        self.argc += 1

    def getArgCount(self):
        return self.argc

    def getArg(self, i):
        if i < self.argc:
            return self.argv[i]
        else:
            return None

    def dump(self, level):
        offset = getDumpOffset(level)
        argStr = ''      
        for i in range(self.argc):
            arg = self.argv[i]
            argValue = arg.getType()+' '+arg.getName()
            argStr += argValue
            if i < (self.argc-1):
                argStr += ","
        print offset + 'function: %s %s (%s)' %(self.retType,self.name,argStr)
        rdbNamedContext.dump(self, level)

#######################
class rdbClassDefn(rdbNamedContext):
    def __init__(self, name):
        rdbNamedContext.__init__(self, name)
        superClass = None

    def getName(self):
        return self.name
    
    def setSuperClass(self, superClass):
        self.superClass = superClass

    def dump(self, level):
        offset = getDumpOffset(level)
        print offset + 'class:'
        rdbNamedContext.dump(self, level)

#######################
class rdbProgram(rdbContext):
    def __init__(self):
        rdbContext.__init__(self)

    def dump(self):
        rdbContext.dump(self, 0)


