from capstone import *
import sys
import re
import global_variable as glv
from terminal_command import TIMEOUT_severalCOMMAND

def tryNtimes(func, time ,args):
    for i in range(time):
        returnValue = eval(func)(args)
        if returnValue!=-1:
            return returnValue
    return -1

def LLVM_mca(input):
    return tryNtimes("LLVM_mcaCore",glv._get("failedRetryTimes"),input)

def LLVM_mcaCore(input):
    sys.stdout.flush()
    command='echo "'+input+'" | '+glv._get("LLVM_mcaPath")+' -iterations='+str(glv._get("BHiveCount"))+" -noalias=false"
    # ic(command)
    outputlist=TIMEOUT_severalCOMMAND(command,glv._get("timeout"))
    # ic(outputlist)
    if outputlist: 
        if len(outputlist)>3:
            regexResult=re.search("Total Cycles:      ([0-9]*)",outputlist[2])
        else:
            regexResult=[]
        if regexResult!=[]:
            resultCycle=regexResult.group(1)
            return resultCycle
        else:
            # print("wrong")
            return -1
    else:
        return -1

def capstone(string):
    CODE = bytes.fromhex(string)
    md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
    InputAsm=""
    for i in md.disasm(CODE, 0x1000):
        # print("%s\t%s" %(i.mnemonic, i.op_str))
        InputAsm+="{}\t{}\n".format(i.mnemonic, i.op_str)
    return InputAsm

def arroundPercent(percent,A,B):
    intA=int(A)
    intB=int(B)
    avg=(intA+intB)/2
    delta=percent*avg/100
    if intA>avg-delta and intA<avg+delta and intB>avg-delta and intB<avg+delta:
        return True
    else:
        return False

def calculateAccuracyLLVM(accurateCycles,predictionCycles):
    accurateCycles=float(accurateCycles)
    predictionCycles=float(predictionCycles)
    if accurateCycles <= 0 or predictionCycles <= 0:
        # print(" rank{}-0".format(rank))
        return 0
    else:
        # print("{} {}".format(accurateCycles,predictionCycles))
        gap=abs(predictionCycles-accurateCycles)
        return gap/accurateCycles # accuracy variable is error