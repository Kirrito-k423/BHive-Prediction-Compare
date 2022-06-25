
def OSACA(password,inputFile,maxOrCP):
    # command='echo '+password+' | python '+OSACAPath+' --arch TSV110 '+str(inputFile)
    command='python '+OSACAPath+' --arch TSV110 '+str(inputFile)
    # print(command)
    list=TIMEOUT_COMMAND(command,glv._get("timeout"))
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
        try:
            if not it:
                return -1
            for match in it: 
                resultList.append(float("0"+match.group()))
            if len(resultList)>2:
                LCD=resultList.pop()
                CP=resultList.pop()
                Max=max(resultList)
                if maxOrCP == "max":
                    return Max
                elif maxOrCP == "CP":
                    return CP
                elif maxOrCP == "LCD":
                    return LCD
                else:
                    return -1
            else:
                return -1
        except Exception as e:
            print("osacaText:{}\n".format(list[resultLineNum]))
            pprint.pprint(list)
            raise e
    else:
        return -1

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
        gap=abs(BHiveCount*predictionCycles-accurateCycles)
        # print(" rank{}-{}".format(rank,int(gap)/int(accurateCycles)))
        return gap/accurateCycles # accuracy variable is error