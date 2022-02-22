from tsjPython.tsjCommonFunc import *
import re
OSACAPath="/home/shaojiemike/github/OSACA-feature-tsv110/newOSACA/bin/osaca "

def OSACA(password,inputFile,maxOrCP):
    val=os.popen('echo '+password+' | sudo -S '+OSACAPath+' --arch TSV110 '+str(inputFile))#  -timeline -show-encoding -all-stats -all-views
    list = val.readlines()
    lineNum=1
    while lineNum:
        listObj=list[lineNum]
        yellowPrint(listObj)
        regexResult=re.search("Loop-Carried Dependencies Analysis Report",listObj)
        if regexResult:
            passPrint(lineNum)
            break
        lineNum+=1
    resultLineNum=lineNum-5
    it=re.finditer("[.0-9]+",list[resultLineNum])
    resultList=[]
    for match in it: 
        print (match.group() )
        resultList.append(float(match.group()))
    print(resultList)
    LCD=resultList.pop()
    TP=resultList.pop()
    print(resultList)
    Max=max(resultList)
    valuePrint(Max)
    valuePrint(TP)
        #     maxresultCycle=regexResult.group(1)
        #     minresultCycle=regexResult.group(2)
        #     avgresultCycle=regexResult.group(3)
        #     CPresultCycle=regexResult.group(4)
        #     # print("before mca {}/{} cycle:{}".format(order,num_file,resultCycle))
        #     # print("  maxresultCycle :{}".format(maxresultCycle))
        #     if maxOrCP == "max":
        #         return maxresultCycle
        #     elif maxOrCP == "CP":
        #         return CPresultCycle
        #     else:
        #         return -1
    # print("  wrong")
    return -1

OSACAInput="/home/shaojiemike/blockFrequency/tmpOSACAfiles/tensorflow_41Gdir_00all_skip_2.0221newOSACA_OSACAInputTmpAsmBlockRank13"
result=OSACA("acsa1411",OSACAInput,"max")
passPrint(result)