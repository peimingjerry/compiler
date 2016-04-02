
from compilerLex import *
from compilerYacc import *
from compilerRDB import *
from compilerDDB import *
import logging

####### databases ########
def getRDB(topFile):
    logging.basicConfig(
        level = logging.DEBUG,
        filename = "parselog.txt",
        filemode = "w",
        format = "%(filename)10s:%(lineno)4d:%(message)s"
    )
    log = logging.getLogger('compilerYacc')

    lexer = lex.lex(module=compilerLex, debug=True)
    try:
        inFile = open(topFile, 'r')
        fs = inFile.read()
        #print fs
    except Exception, err:
        print err
    lexer.input(fs)
     
    parser = yacc.yacc(errorlog=log)
    parser.parse(lexer=lexer, debug=False)

    return rdbTop

        
####### Main ########
def main():
    program_rdb = getRDB('input.cpp')
    print '\n----------------------\nRDB:'
    program_rdb.dump()
    print '----------------------\n'
    program_ddb = ddbProgram (program_rdb)
    program_ddb.elaborate()
    print '\n----------------------\nDDB:'
    program_ddb.dump()
    print '----------------------\n'
    
if __name__ == '__main__':
    main()
