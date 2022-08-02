
def OSACA(inputFile):

    if glv._get("useOSACAHistoryData")=="yes" and glv._get("isPageExisted")=="yes":
        if block in glv._get("historyDict").dataDict["unique_revBiblock"]:
            return [glv._get("historyDict").dataDict["OSACA_CPLCDmax_CyclesRevBiBlock"][block],\
                    glv._get("historyDict").dataDict["OSACA_CPLCDavg_CyclesRevBiBlock"][block],\
                    glv._get("historyDict").dataDict["OSACACPCyclesRevBiBlock"][block],\
                    glv._get("historyDict").dataDict["OSACALCDCyclesRevBiBlock"][block]]

    command='python '+OSACAPath+' --arch TSV110 '+str(inputFile)
    ic(command)
    list=TIMEOUT_COMMAND(command,glv._get("timeout"))
    try:
        if list and len(list)>1:
            lineNum=1
            while lineNum:
                listObj=list[lineNum]
                regexResult=re.search("Loop-Carried Dependencies Analysis Report",listObj)
                if regexResult:
                    break
                lineNum+=1
            resultLineNum=lineNum-5
            it=re.finditer("[.0-9]+",list[resultLineNum])
            resultList=[]
            if not it:
                return -1
            for match in it: 
                resultList.append(float("0"+match.group()))
            if len(resultList)>2:
                LCD=resultList.pop()
                CP=resultList.pop()
                Max=max(resultList)
                AVG=(LCD+CP)*1.0/2
                return [Max, AVG, CP, LCD]
            else:
                return [-1,-1,-1,-1]
        else:
            return [-1,-1,-1,-1]
    except Exception as e:
        print("osacaText:{}\n".format(list[resultLineNum]))
        pprint.pprint(list)
        raise e
    

def saveOSACAInput2File(InputAsmList,rank):
    writeFilename="{}/tmpOSACAfiles/{}.{}_OSACAInputTmpAsmBlockRank{}".format(taskfilePath,taskfilenameprefixWithoutPath,saveInfo,rank)
    fwriteblockfreq = open(writeFilename, "w")
    for tmp_InputAsmList in InputAsmList:
        fwriteblockfreq.writelines(tmp_InputAsmList)
    fwriteblockfreq.close()
    return writeFilename

def capstoneList(string):
    CODE = bytes.fromhex(string)
    md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
    InputAsmList=[]
    for i in md.disasm(CODE, 0x1000):
        # print("%s\t%s" %(i.mnemonic, i.op_str))
        InputAsmList.append("{}\t{}\n".format(i.mnemonic, i.op_str))
    return InputAsmList

def capstoneInput(block):
    input2word=""
    for i in range(int((len(block)+1)/9)):
        # print(i)
        input2word+=block[i*9:i*9+2]+block[i*9+2:i*9+4]
        input2word+=block[i*9+4:i*9+6]+block[i*9+6:i*9+8]
    return input2word


def calculateAccuracyOSACA(accurateCycles,predictionCycles,rank):
    # print(" rank{}-tsj".format(rank))
    accurateCycles=float(accurateCycles)
    predictionCycles=float(predictionCycles)
    if accurateCycles <= 0 or predictionCycles <= 0:
        # print(" rank{}-0".format(rank))
        return 0
    else:
        # print(" rank{}-tsj2".format(rank))
        # print("{} {}".format(accurateCycles,predictionCycles))
        gap=abs(glv._get("BHiveCount")*predictionCycles-accurateCycles)
        # print(" rank{}-{}".format(rank,int(gap)/int(accurateCycles)))
        return gap/accurateCycles # accuracy variable is error