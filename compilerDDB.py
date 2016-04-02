
from util import *
from compilerRDB import *

############################
class ddbParam:
    def __init__(self, obj):
        self.rdbObj = obj
        
    def getValue(self):
        return self.rdbObj.value

    def getRefVar(self):
        return self.rdbObj.refVar

    def isRefValue(self):
        return (self.rdbObj.valueType == 'RefVar')

    def valueToStr(self):
        paramValue = ''
        if self.rdbObj.isRefValue():
            paramValue = self.rdbObj.getRefVar()
        else:
            paramValue = str(self.rdbObj.getValue())
        return paramValue

#######################
class ddbFuncCall:
    def __init__(self):
        self.rdbObj = None
        self.master = None
        self.parent = None
        self.params = list()
        self.paramCount = 0
        self.is_from_mem_func = False

    def setRdbObj(self, rdbObj):
        self.rdbObj = rdbObj

    def getRdbObj(self):
        return self.rdbObj
    
    def setMaster(self, master):
        self.master = master
        
    def getMaster(self):
        return self.master

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent
    
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

    def setFromMemFunc(self, flag):
        self.is_from_mem_func = flag
        
    def isFromMemFunc(self):
        return self.is_from_mem_func

    def dump(self, level):
        offset = getDumpOffset(level)
        paramsStr = ''
        for i in range(self.paramCount):
            param = self.params[i]
            if self.isFromMemFunc() and i==0:
                #print param
                paramsStr += "this= %s" % param.getName()
            else:
                if isinstance(param, ddbVar):
                    paramValue = param.getName()
                else:
                    paramValue = str(param)
                paramsStr += paramValue
            if i < (self.paramCount-1):
                paramsStr += ", "
        masterStr = ''
        if self.master != None:
            masterStr = self.master.getName()
        print offset + 'calling function: %s(%s)' % (masterStr,paramsStr)

#######################
class ddbAsignExpr:
    def __init__(self):
        self.rdbObj = None
        self.paramL = None
        self.paramR = None
        self.parent = None

    def setRdbObj(self, rdbObj):
        self.rdbObj = rdbObj

    def getRdbObj(self):
        return self.rdbObj
    
    def setParamL(self, paramL):
        self.paramL = paramL
        
    def setParamR(self, paramR):
        self.paramR = paramR
        
    def getParamL(self):
        return self.paramL

    def getParamR(self):
        return self.paramR
    
    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def dump(self, level):
        offset = getDumpOffset(level)
        lstr = self.paramL.getName()
        rstr = ''
        if isinstance(self.paramR, ddbVar):
            rstr = self.paramR.getName()
        else:
            rstr = str(self.paramR)
        print offset + 'excute: %s = %s' % (lstr, rstr)

#######################
class ddbVar:
    #TODO: call constructor with parameters
    def __init__(self, name,):
        self.name = name
        self.rdbObj = None
        self.master = None
        self.parent = None

    def setRdbObj(self, rdbObj):
        self.rdbObj = rdbObj

    def getRdbObj(self):
        return self.rdbObj
        
    def getName(self):
        return self.name

    def setMaster(self, master):
        self.master = master

    def getMaster(self):
        return self.master

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent
    
    def dump(self, level):
        offset = getDumpOffset(level)
        masterName = ''
        if self.master != None:
            masterName = self.master.getName()
        print offset + 'name = %s   master =  %s' % (self.name, masterName)

#######################
class BasicType:
    def __init__(self, name):
        self.name = name
        self.isBasicType = True

    def getName(self):
        return self.name

    def dump(self, level):
        offset = getDumpOffset(level)
        print offset + 'BuiltIn type: %s' % self.name
        
#######################
class Integer(BasicType):
    def __init__(self):
        BasicType.__init__ (self, 'int')

#######################
class Char(BasicType):
    def __init__(self):
        BasicType.__init__ (self, 'char')        
        
#######################       
class ddbContext:
    def __init__(self,):
        self.parent = None
        self.rdbObj = None
        self.vars = list()
        self.instructions = list()
        self.funcDefns = list()
        self.classDefns = list()
        self.isElab = False
        #TODO: use set to find duplicated defns. need to check the overload func

    def setRdbObj(self, rdbObj):
        self.rdbObj = rdbObj

    def getRdbObj(self):
        return self.rdbObj
    
    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent
    
    def addVar(self, var):
        self.vars.append(var)

    def findVar(self, var):
        parent = self
        while parent != None:
            foundVar = parent.findVar_(var)
            if foundVar != None:
                return foundVar
            parent = parent.getParent()
        return None
            
    def findVar_(self, var):
        for i in self.vars:
            if i.getName() == var:
                return i
        return None
        
    def addInstruction(self, instruction):
        self.instructions.append(instruction)

    def getInstructions(self):
        return self.instructions

    def addFuncDefn(self, funcDefn):
        self.funcDefns.append(funcDefn)

    def addClassDefn(self, classDefn):
        self.classDefns.append(classDefn)

    def findClassDefn(self, className):
        parent = self
        while parent != None:
            foundVar = parent.findClassDefn_(className)
            if foundVar != None:
                return foundVar
            parent = parent.getParent()
        return None
    
    def findClassDefn_(self, className):
        for i in self.classDefns:
            if i.getName() == className:
                return i
        return None

    def findFuncDefn(self, funcDefnName):
        parent = self
        while parent != None:
            foundVar = parent.findFuncDefn_(funcDefnName)
            if foundVar != None:
                return foundVar
            parent = parent.getParent()
        return None
    
    def findFuncDefn_(self, funcDefnName):
        for i in self.funcDefns:
            if i.getName() == funcDefnName:
                return i
        return None
    
    def findMainFuncDefn(self):
        return self.findFuncDefn('main')

    def setElaborated(self, isElab):
        self.isElab = isElab
        
    def isElaborated(self):
        return self.isElab
    
    def elaborate(self):
        self.populateMasters()
        self.populateInstances()
        self.bindInstances()
    
    def populateMasters(self):
        rdbObj = self.rdbObj
        if rdbObj == None:
            print self
        assert rdbObj != None
        for i in rdbObj.getFuncDefns():
            if i.isMemberFunc():
                newName = self.name + '_' + i.getName()
                func = ddbFuncDefn(newName, i.getRetType())
                func.setRdbObj(i)
                func.setFromMemFunc(True)
                # add this pointer
                param = ddbVar('this')
                param.setRdbObj(None)
                param.setMaster(self)
                param.setParent(func)
                func.addArg(param)
                # add as global function
                parent = self
                while True:
                    if isinstance(parent, ddbProgram):
                        func.setParent(parent)
                        parent.addFuncDefn(func)
                        break
                    else:
                        parent = parent.getParent()
            else:
                func = ddbFuncDefn(i.getName(), i.getRetType())
                func.setRdbObj(i)
                func.setParent(self)
                self.addFuncDefn(func)
            for j in range(i.getArgCount()):
                rdb_param = i.getArg(j)
                param = ddbVar(rdb_param.getName())
                param.setRdbObj(rdb_param)
                param.setParent(func)
                func.addArg(param)
        for i in rdbObj.getClassDefns():
            classDefn = ddbClassDefn(i.getName())
            classDefn.setRdbObj(i)
            classDefn.setParent(self)
            self.addClassDefn(classDefn)

    def populateInstances(self):
        rdbObj = self.rdbObj
        assert rdbObj != None
        for i in rdbObj.getVars():
            inst = ddbVar(i.getName())
            inst.setRdbObj(i)
            inst.setParent(self)
            self.addVar(inst)
        for i in rdbObj.getInstructions():
            if isinstance(i, rdbFuncCall):
                inst = ddbFuncCall()
            elif isinstance(i, rdbAsignExpr):
                inst = ddbAsignExpr()
            inst.setRdbObj(i)
            inst.setParent(self)
            self.addInstruction(inst)
            
    def bindInstances(self):
        for inst in self.vars:
            rdbInst = inst.getRdbObj()
            # find the master
            masterName = rdbInst.getType()
            parent = inst.getParent()
            foundClassDefn = parent.findClassDefn(masterName)
            if foundClassDefn != None:
                inst.setMaster(foundClassDefn)
                if not isinstance(foundClassDefn, BasicType):
                     #   elaborate the master if not elaborated
                     if not foundClassDefn.isElaborated():
                        foundClassDefn.elaborate()
                        foundClassDefn.setElaborated(True)
            else:
                print 'Cannot find master with name %s' % masterName
        for inst in self.instructions:
            if isinstance(inst, ddbFuncCall):
                rdb_func_call = inst.getRdbObj()
                # find function master
                funcName = rdb_func_call.getName() 
                parent = inst.getParent()
                foundFunc = None
                if not '.' in funcName:
                    foundFunc = parent.findFuncDefn(funcName)
                    if foundFunc != None:
                        inst.setMaster(foundFunc)
                    else:
                        print 'cannot  find function with name %s' % funcName     
                else:                   
                    slices = funcName.split('.')
                    #TODO: slices may be more than two, like hier-node
                    objName = slices[0]  
                    funcName = slices[1] 
                    foundVar = parent.findVar(objName)
                    #print 'objName=' + objName
                    #print 'funcName=' + funcName
                    if foundVar != None:
                        varClass = foundVar.getMaster()
                        funcName = varClass.getName() + '_' + funcName
                        foundFunc = parent.findFuncDefn(funcName)
                        if foundFunc != None:
                            inst.addParam(foundVar)
                            inst.setMaster(foundFunc)
                            inst.setFromMemFunc(True)
                        else:
                            print 'cannot  find function with name %s' % funcName
                    else:
                        print 'cannot  find variable with name %s' % objName               
                # find parameters
                for i in range(rdb_func_call.getParamCount()):
                    rdb_param = rdb_func_call.getParam(i)
                    if rdb_param.isRefValue():
                        value = rdb_param.getRefVar()
                        parent = inst.getParent()
                        foundVar = parent.findVar(value)
                        if foundVar != None:
                            inst.addParam(foundVar)
                        else:
                            print 'cannot  find parameter with name %s in function %s' % (value, funcName)
                    else:
                        value = rdb_param.getValue()
                        inst.addParam(value)
                if foundFunc != None:
                    if not foundFunc.isElaborated():
                        #print '\nTo elaborate function: ' + foundFunc.getName() + '\n'
                        foundFunc.elaborate()
                        foundFunc.setElaborated(True)
            else:
                # assign expr handling
                rdb_expr = inst.getRdbObj()
                parent = inst.getParent()
                paramL = rdb_expr.getParamL()
                paramR = rdb_expr.getParamR()
                assert paramL.isRefValue()             
                foundVar = parent.findVar(paramL.getRefVar())
                if foundVar != None:
                    inst.setParamL(foundVar)
                else:
                    print 'cannot find L value of expr %s' % paramL.getRefVar()
                if paramR.isRefValue():
                    foundVar = parent.findVar(paramR.getRefVar())
                    if foundVar != None:
                        inst.setParamR(foundVar)
                    else:
                        print 'cannot find R value of expr %s' % paramR.getRefVar()
                else:
                    inst.setParamR(paramR.getValue())
                    
    def dump(self, level):
        offset = getDumpOffset(level-1)
        print offset + '{'
        offset = getDumpOffset(level)
        offsetContent = getDumpOffset(level+1)
        if len(self.classDefns) != 0:
            print offset+'classDefns:'
            for i in self.classDefns:
                i.dump(level+1)
        if len(self.funcDefns) != 0:
            print offset+'funcDefns:'
            for i in self.funcDefns:
                i.dump(level+1)
        if len(self.vars) != 0:
            print offset+'vars:'
            for i in self.vars:
                i.dump(level+1)
        if len(self.instructions) != 0:
            print offset+'instructions:'
            for i in self.instructions:
                i.dump(level+1)
        offset = getDumpOffset(level-1)
        print offset + '}'

#######################       
class ddbNamedContext(ddbContext):
    def __init__(self, name):
        ddbContext.__init__(self)
        self.name = name

    def getName(self):
        return self.name

##    def elaborate(self):
##        print 'elaborating %s' % self.name
##        ddbContext.elaborate(self)
    
    def dump(self, level):
        offset = getDumpOffset(level)
        print offset + self.name
        ddbContext.dump(self, level+1)

#######################         
class ddbFuncDefn(ddbNamedContext):
    def __init__(self, name, retType):
        ddbNamedContext.__init__(self, name)
        self.retType = retType
        self.argv = list()
        self.argc = 0
        self.is_from_mem_func = False

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

    def setFromMemFunc(self, flag):
        self.is_from_mem_func = flag
        
    def isFromMemFunc(self):
        return self.is_from_mem_func

    def findVar_(self, var):
        for i in self.vars:
            if i.getName() == var:
                return i
        for i in self.argv:
            if i.getName() == var:
                return i
        if self.isFromMemFunc():
            parentObj = self.getArg(0)
            parentClass = parentObj.getMaster()
            assert isinstance(parentClass, ddbClassDefn)
            return parentClass.findVar(var)
        return None
    
    def elaborate(self):
        if self.isFromMemFunc():
            # Change the member variables with this pointer
            pass
        ddbNamedContext.elaborate(self)
        
    def dump(self, level):
        offset = getDumpOffset(level)
        argStr = ''      
        for i in range(self.argc):
            arg = self.argv[i]
            master = arg.getMaster()
            if master != None:
                argValue = master.getName()+' '+arg.getName()
            else:
                argValue = arg.getRdbObj().getType()+' '+arg.getName()
            argStr += argValue
            if i < (self.argc-1):
                argStr += ","
        print offset + 'function: %s %s (%s)' %(self.retType,self.name,argStr)
        ddbNamedContext.dump(self, level)
        
#######################
class ddbMainFuncDefn(ddbFuncDefn):
    def __init__(self, retType):
        ddbFuncDefn.__init__(self, 'main', retType)

#######################        
class ddbClassDefn(ddbNamedContext):
    def __init__(self, name):
        ddbNamedContext.__init__(self, name)
        superClass = None
    
    def setSuperClass(self, superClass):
        self.superClass = superClass

    def getSuperClass(self):
        return self.superClass

    def dump(self, level):
        offset = getDumpOffset(level)
        print offset + 'class:'
        ddbNamedContext.dump(self, level)
       
#######################
class ddbProgram(ddbContext):
    def __init__(self, rdbObj):
        ddbContext.__init__(self)
        ddbContext.setRdbObj(self, rdbObj)

    def populateMasters(self):
        self.populateBuiltInTypes()
        ddbContext.populateMasters(self)

    def populateBuiltInTypes(self):
        self.classDefns.append(Integer())
        self.classDefns.append(Char())
        
    def elaborate(self):
        self.populateMasters()
        self.populateInstances()
        self.bindInstances()
        mainFuncDefn = self.findMainFuncDefn()
        if mainFuncDefn != None:
            mainFuncCall = ddbFuncCall()
            mainFuncCall.setMaster(mainFuncDefn)
            self.instructions.append(mainFuncCall)
            mainFuncDefn.elaborate()

    def dump(self):
        ddbContext.dump(self, 0)
