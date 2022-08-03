from terminal_command import TIMEOUT_COMMAND
import sys
import global_variable as glv
import re
import time

def tryNtimes(func, RetryTime ,args):
    for i in range(RetryTime):
        returnValue = eval(func)(args)
        if returnValue!=-1:
            return returnValue
        time.sleep(glv._get("failedSleepTime"))
    return -1

def BHiveResultStable(input):
    firstResult=-2
    returnResult=tryNtimes("BHiveCore",glv._get("failedRetryTimes"),input)
    tryTimes=0
    while returnResult != firstResult and tryTimes < glv._get("failedRetryTimes")+5:
        if firstResult == -2 or returnResult != -1:
            firstResult=returnResult
        returnResult=tryNtimes("BHiveCore",glv._get("failedRetryTimes"),input)
        tryTimes += 1
    return firstResult

def BHive(block,input):
    if glv._get("useBhiveHistoryData")=="yes" and glv._get("isPageExisted")=="yes":
        if block in glv._get("historyDict").dataDict["unique_revBiblock"]:
            return glv._get("historyDict").dataDict["BhiveCyclesRevBiBlock"][block]
    return BHiveResultStable(input)

def BHiveCore(input):
    sys.stdout.flush()
    command=glv._get("BHivePath")+' '+input+" "+str(glv._get("BHiveCount"))
    list=TIMEOUT_COMMAND(command,glv._get("timeout"))
    ic(list)

    if list is None or len(list)==0:
        regexResult=None
    else:
        regexResult=re.search("Event num: ([0-9]*)",list[-1])
    if regexResult:
        resultCycle=regexResult.group(1)
        return resultCycle
    return -1

def BHiveInput(block):
    input2word=""
    for i in range(int((len(block)+1)/9)):
        input2word+=" 0x"+block[i*9:i*9+2]+" 0x"+block[i*9+2:i*9+4]
        input2word+=" 0x"+block[i*9+4:i*9+6]+" 0x"+block[i*9+6:i*9+8]
    return input2word

def BHiveInputDel0xSpace(block):
    input2word=""
    for i in range(int((len(block)+1)/9)):
        input2word+=block[i*9:i*9+2]+block[i*9+2:i*9+4]
        input2word+=block[i*9+4:i*9+6]+block[i*9+6:i*9+8]
    return input2word

def BHiveInputDel0x(block):
    input2word=""
    for i in range(int((len(block)+1)/9)):
        input2word+=" "+block[i*9:i*9+2]+" "+block[i*9+2:i*9+4]
        input2word+=" "+block[i*9+4:i*9+6]+" "+block[i*9+6:i*9+8]
    return input2word

def BHiveInputDelimiter(block):
    Delimiter="x"
    input2word=""
    for i in range(int((len(block)+1)/9)):
        input2word+=Delimiter+block[i*9:i*9+2]+Delimiter+block[i*9+2:i*9+4]
        input2word+=Delimiter+block[i*9+4:i*9+6]+Delimiter+block[i*9+6:i*9+8]
    return input2word